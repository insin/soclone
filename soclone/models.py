"""SOClone Models."""
import datetime
import hashlib
import re

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import connection, models, transaction
from django.db.models import Q
from django.db.models.signals import post_delete, post_save, pre_save
from django.template.defaultfilters import slugify
from django.utils import simplejson

class TagManager(models.Manager):
    UPDATE_USE_COUNTS_QUERY = (
        'UPDATE soclone_tag '
        'SET use_count = ('
            'SELECT COUNT(*) FROM soclone_question_tags '
            'WHERE tag_id = soclone_tag.id'
        ') '
        'WHERE id IN (%s)')

    def get_or_create_multiple(self, names, user):
        """
        Fetches a list of Tags with the given names, creating any Tags
        which don't exist when necesssary.
        """
        tags = list(self.filter(name__in=names))
        if len(tags) < len(names):
            existing_names = set(tag.name for tag in tags)
            new_names = [name for name in names if name not in existing_names]
            tags.extend([self.create(name=name, created_by=user)
                         for name in new_names])
        return tags

    def update_use_counts(self, tags):
        """Updates the given Tags with their current use counts."""
        if not tags:
            return
        cursor = connection.cursor()
        query = self.UPDATE_USE_COUNTS_QUERY % ','.join(['%s'] * len(tags))
        cursor.execute(query, [tag.id for tag in tags])
        transaction.commit_unless_managed()

class Tag(models.Model):
    """A tag for Questions."""
    name       = models.CharField(max_length=24, unique=True)
    created_by = models.ForeignKey(User, related_name='created_tags')
    # Denormalised data
    use_count = models.PositiveIntegerField(default=0)

    objects = TagManager()

    class Meta:
        ordering = ('-use_count', 'name')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', args=[self.name])

class QuestionManager(models.Manager):
    def update_tags(self, question, tagnames, user):
        """
        Updates Tag associations for a question to match the given
        tagname string.

        Returns ``True`` if tag usage counts were updated as a result,
        ``False`` otherwise.
        """
        current_tags = list(question.tags.all())
        current_tagnames = set(t.name for t in current_tags)
        updated_tagnames = set(t for t in tagnames.split(' ') if t)
        modified_tags = []

        removed_tags = [t for t in current_tags
                        if t.name not in updated_tagnames]
        if removed_tags:
            modified_tags.extend(removed_tags)
            question.tags.remove(*removed_tags)

        added_tagnames = updated_tagnames - current_tagnames
        if added_tagnames:
            added_tags = Tag.objects.get_or_create_multiple(added_tagnames,
                                                            user)
            modified_tags.extend(added_tags)
            question.tags.add(*added_tags)

        if modified_tags:
            Tag.objects.update_use_counts(modified_tags)
            return True

        return False

    def update_answer_count(self, question):
        """
        Executes an UPDATE query to update denormalised data with the
        number of answers the given question has.
        """
        self.filter(id=question.id).update(
            answer_count=Answer.objects.for_question(question).count())

class Question(models.Model):
    CLOSE_REASONS = (
        (1, u'Exact duplicate'),
        (2, u'Not programming related'),
        (3, u'Subjective and argumentative'),
        (4, u'Not a real question'),
        (5, u'Blatantly offensive'),
        (6, u'No longer relevant'),
        (7, u'Too localized'),
        (8, u'Spam'),
    )

    """A question."""
    title    = models.CharField(max_length=300)
    author   = models.ForeignKey(User, related_name='questions')
    added_at = models.DateTimeField(default=datetime.datetime.now)
    tags     = models.ManyToManyField(Tag, related_name='questions')
    # Status
    wiki            = models.BooleanField(default=False)
    answer_accepted = models.BooleanField(default=False)
    closed          = models.BooleanField(default=False)
    closed_by       = models.ForeignKey(User, null=True, blank=True, related_name='closed_questions')
    closed_at       = models.DateTimeField(null=True, blank=True)
    close_reason    = models.SmallIntegerField(choices=CLOSE_REASONS, null=True, blank=True)
    deleted         = models.BooleanField(default=False)
    deleted_at      = models.DateTimeField(null=True, blank=True)
    deleted_by      = models.ForeignKey(User, null=True, blank=True, related_name='deleted_questions')
    locked          = models.BooleanField(default=False)
    locked_by       = models.ForeignKey(User, null=True, blank=True, related_name='locked_questions')
    locked_at       = models.DateTimeField(null=True, blank=True)
    # Denormalised data
    score                = models.IntegerField(default=0)
    answer_count         = models.PositiveIntegerField(default=0)
    comment_count        = models.PositiveIntegerField(default=0)
    view_count           = models.PositiveIntegerField(default=0)
    offensive_flag_count = models.SmallIntegerField(default=0)
    favourite_count      = models.PositiveIntegerField(default=0)
    last_edited_at       = models.DateTimeField(null=True, blank=True)
    last_edited_by       = models.ForeignKey(User, null=True, blank=True, related_name='last_edited_questions')
    last_activity_at     = models.DateTimeField()
    last_activity_by     = models.ForeignKey(User, related_name='last_active_in_questions')
    tagnames             = models.CharField(max_length=125)
    summary              = models.CharField(max_length=180)
    html                 = models.TextField()

    objects = QuestionManager()

    def save(self, **kwargs):
        """
        Overridden to manually manage addition of tags when the object
        is first saved.

        This is required as we're using ``tagnames`` as the sole means of
        adding and editing tags.
        """
        initial_addition = (self.id is None)
        super(Question, self).save(**kwargs)
        if initial_addition:
            tags = Tag.objects.get_or_create_multiple(self.tagname_list(),
                                                      self.author)
            self.tags.add(*tags)
            Tag.objects.update_use_counts(tags)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '%s%s/' % (reverse('question', args=[self.id]),
                          slugify(self.title))

    def get_revision_url(self):
        return reverse('question_revisions', args=[self.id])

    def get_latest_revision(self):
        """Convenience method to grab the latest revision."""
        return self.revisions.all()[0]

    def tagname_list(self):
        """Creates a list of Tag names from the ``tagnames`` attribute."""
        return [name for name in self.tagnames.split(u' ')]

class QuestionRevision(models.Model):
    """A revision of a Question."""
    question   = models.ForeignKey(Question, related_name='revisions')
    revision   = models.PositiveIntegerField(blank=True)
    title      = models.CharField(max_length=300)
    author     = models.ForeignKey(User, related_name='question_revisions')
    revised_at = models.DateTimeField()
    tagnames   = models.CharField(max_length=125)
    summary    = models.CharField(max_length=300, blank=True)
    text       = models.TextField()

    class Meta:
        ordering = ('-revision',)

    def save(self, **kwargs):
        """Looks up the next available revision number."""
        if not self.revision:
            self.revision = QuestionRevision.objects.filter(
                question=self.question).values_list('revision',
                                                    flat=True)[0] + 1
        super(QuestionRevision, self).save(**kwargs)

    def __unicode__(self):
        return u'revision %s of %s' % (self.revision, self.title)

class FavouriteQuestion(models.Model):
    """A favourite Question of a User."""
    question      = models.ForeignKey(Question)
    user          = models.ForeignKey(User)
    favourited_at = models.DateTimeField(default=datetime.datetime.now)

def update_question_favourite_count(instance, **kwargs):
    """
    Updates the favourite count for the Question related to the given
    FavouriteQuestion.
    """
    if kwargs.get('raw', False):
        return
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE soclone_question SET favourite_count = ('
            'SELECT COUNT(*) from soclone_favouritequestion '
            'WHERE soclone_favouritequestion.question_id = soclone_question.id'
        ') '
        'WHERE id = %s', [instance.question_id])
    transaction.commit_unless_managed()

post_save.connect(update_question_favourite_count, sender=FavouriteQuestion)
post_delete.connect(update_question_favourite_count, sender=FavouriteQuestion)

class AnswerManager(models.Manager):
    def for_question(self, question, user=None):
        """
        Retrieves visibile answers for the given question. Delete answers
        are only visibile to the person who deleted them.
        """
        if user is None or not user.is_authenticated():
            return self.filter(question=question, deleted=False)
        else:
            return self.filter(Q(question=question),
                               Q(deleted=False) | Q(deleted_by=user))

class Answer(models.Model):
    """An answer to a Question."""
    question = models.ForeignKey(Question, related_name='answers')
    author   = models.ForeignKey(User, related_name='answers')
    added_at = models.DateTimeField(default=datetime.datetime.now)
    # Status
    wiki        = models.BooleanField(default=False)
    accepted    = models.BooleanField(default=False)
    deleted     = models.BooleanField(default=False)
    deleted_by  = models.ForeignKey(User, null=True, blank=True, related_name='deleted_answers')
    locked      = models.BooleanField(default=False)
    locked_by   = models.ForeignKey(User, null=True, blank=True, related_name='locked_answers')
    locked_at   = models.DateTimeField(null=True, blank=True)
    # Denormalised data
    score                = models.IntegerField(default=0)
    comment_count        = models.PositiveIntegerField(default=0)
    offensive_flag_count = models.SmallIntegerField(default=0)
    last_edited_at       = models.DateTimeField(null=True, blank=True)
    last_edited_by       = models.ForeignKey(User, null=True, blank=True, related_name='last_edited_answers')
    html                 = models.TextField()

    objects = AnswerManager()

    def get_absolute_url(self):
        return reverse('answer', args=[self.id])

    def get_latest_revision(self):
        """Convenience method to grab the latest revision."""
        return self.revisions.all()[0]

class AnswerRevision(models.Model):
    """A revision of an Answer."""
    answer     = models.ForeignKey(Answer, related_name='revisions')
    revision   = models.PositiveIntegerField()
    author     = models.ForeignKey(User, related_name='answer_revisions')
    revised_at = models.DateTimeField()
    summary    = models.CharField(max_length=300, blank=True)
    text       = models.TextField()

    class Meta:
        ordering = ('-revision',)

    def save(self, **kwargs):
        """Looks up the next available revision number if not set."""
        if not self.revision:
            self.revision = AnswerRevision.objects.filter(
                answer=self.answer).values_list('revision',
                                                flat=True)[0] + 1
        super(AnswerRevision, self).save(**kwargs)

class Vote(models.Model):
    """An up or down vote on a Question or Answer."""
    VOTE_UP = +1
    VOTE_DOWN = -1
    VOTE_CHOICES = (
        (VOTE_UP,   u'Up'),
        (VOTE_DOWN, u'Down'),
    )

    content_type   = models.ForeignKey(ContentType)
    object_id      = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    user           = models.ForeignKey(User, related_name='votes')
    vote           = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('content_type', 'object_id', 'user')

    def is_upvote(self):
        return self.vote == self.VOTE_UP

    def is_downvote(self):
        return self.vote == self.VOTE_UP

def update_post_score(instance, **kwargs):
    """
    Updates the score for the Question or Answer related to the given
    Vote.
    """
    if kwargs.get('raw', False):
        return
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE %(post_table)s SET score = ('
            'SELECT SUM(vote) from soclone_vote '
            'WHERE soclone_vote.content_type_id = %%s '
              'AND soclone_vote.object_id = %(post_table)s.id'
        ') '
        'WHERE id = %%s' % {
            'post_table': instance.content_type.model_class()._meta.db_table,
        }, [instance.content_type_id, instance.object_id])
    transaction.commit_unless_managed()

post_save.connect(update_post_score, sender=Vote)
post_delete.connect(update_post_score, sender=Vote)

class Comment(models.Model):
    """A comment on a Question or Answer."""
    content_type   = models.ForeignKey(ContentType)
    object_id      = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    user           = models.ForeignKey(User, related_name='comments')
    comment        = models.CharField(max_length=300)
    added_at       = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        ordering = ('-added_at',)

def update_post_comment_count(instance, **kwargs):
    """
    Updates the comment count for the Question or Answer related to the
    given Comment.
    """
    if kwargs.get('raw', False):
        return
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE %(post_table)s SET comment_count = ('
            'SELECT COUNT(*) from soclone_comment '
            'WHERE soclone_comment.content_type_id = %%s '
              'AND soclone_comment.object_id = %(post_table)s.id'
        ') '
        'WHERE id = %%s' % {
            'post_table': instance.content_type.model_class()._meta.db_table,
        }, [instance.content_type_id, instance.object_id])
    transaction.commit_unless_managed()

post_save.connect(update_post_comment_count, sender=Comment)
post_delete.connect(update_post_comment_count, sender=Comment)

class FlaggedItem(models.Model):
    """A flag on a Question or Answer indicating offensive content."""
    content_type   = models.ForeignKey(ContentType)
    object_id      = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    user           = models.ForeignKey(User, related_name='flagged_items')
    flagged_at     = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        unique_together = ('content_type', 'object_id', 'user')

def update_post_offensive_flag_count(instance, **kwargs):
    """
    Updates the offensive flag count for the Question or Answer related
    to the given FlaggedItem.
    """
    if kwargs.get('raw', False):
        return
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE %(post_table)s SET offensive_flag_count = ('
            'SELECT COUNT(*) from soclone_flaggeditem '
            'WHERE soclone_flaggeditem.content_type_id = %%s '
              'AND soclone_flaggeditem.object_id = %(post_table)s.id'
        ') '
        'WHERE id = %%s' % {
            'post_table': instance.content_type.model_class()._meta.db_table,
        }, [instance.content_type_id, instance.object_id])
    transaction.commit_unless_managed()

post_save.connect(update_post_offensive_flag_count, sender=FlaggedItem)
post_delete.connect(update_post_offensive_flag_count, sender=FlaggedItem)

class Badge(models.Model):
    """Awarded for notable actions performed on the site by Users."""
    GOLD = 1
    SILVER = 2
    BRONZE = 3
    TYPE_CHOICES = (
        (GOLD,   u'gold'),
        (SILVER, u'silver'),
        (BRONZE, u'bronze'),
    )

    name        = models.CharField(max_length=50)
    type        = models.SmallIntegerField(choices=TYPE_CHOICES)
    slug        = models.SlugField(max_length=50, blank=True)
    description = models.CharField(max_length=300)
    multiple    = models.BooleanField(default=False)
    # Denormalised data
    awarded_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('name',)
        unique_together = ('name', 'type')

    def __unicode__(self):
        return u'%s badge: %s' % (self.get_type_display(), self.name)

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Badge, self).save(**kwargs)

    def get_absolute_url(self):
        return '%s%s/' % (reverse('badge', args=[self.id]), self.slug)

class Award(models.Model):
    """The awarding of a Badge to a User."""
    user       = models.ForeignKey(User)
    badge      = models.ForeignKey(Badge)
    awarded_at = models.DateTimeField(default=datetime.datetime.now)
    notified   = models.BooleanField(default=False)

def update_badge_award_counts(instance, **kwargs):
    """
    Updates the awarded count for the Badge and User related to the given
    Award.
    """
    if kwargs.get('raw', False):
        return
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE auth_user SET %s = ('
            'SELECT COUNT(*) FROM soclone_award '
            'INNER JOIN soclone_badge '
                'ON soclone_badge.id = soclone_award.badge_id '
                'AND soclone_badge.type = %%s '
            'WHERE soclone_award.user_id = auth_user.id'
        ') '
        'WHERE id = %%s' % dict(Badge.TYPE_CHOICES)[instance.badge.type],
        [instance.badge.type, instance.user_id])
    cursor.execute(
        'UPDATE soclone_badge SET awarded_count = ('
            'SELECT COUNT(*) FROM soclone_award '
            'WHERE soclone_award.badge_id = soclone_badge.id'
        ') '
        'WHERE id = %%s', [instance.badge_id])
    transaction.commit_unless_managed()

post_save.connect(update_badge_award_counts, sender=Award)
post_delete.connect(update_badge_award_counts, sender=Award)

# Here be Drago^H^H^H^H^HMonkeys

QUESTIONS_PER_PAGE_CHOICES = (
   (10, u'10'),
   (30, u'30'),
   (50, u'50'),
)

# Monkeypatch additional profile fields into User
User.add_to_class('reputation', models.PositiveIntegerField(default=1))
User.add_to_class('gravatar', models.CharField(max_length=32))
User.add_to_class('favourite_questions',
                  models.ManyToManyField(Question, through=FavouriteQuestion,
                                         related_name='favourited_by'))
User.add_to_class('badges', models.ManyToManyField(Badge, through=Award,
                                                   related_name='awarded_to'))
User.add_to_class('gold', models.SmallIntegerField(default=0))
User.add_to_class('silver', models.SmallIntegerField(default=0))
User.add_to_class('bronze', models.SmallIntegerField(default=0))
User.add_to_class('questions_per_page',
                  models.SmallIntegerField(choices=QUESTIONS_PER_PAGE_CHOICES, default=10))
User.add_to_class('last_seen',
                  models.DateTimeField(default=datetime.datetime.now))
User.add_to_class('real_name', models.CharField(max_length=100, blank=True))
User.add_to_class('website', models.URLField(max_length=200, blank=True))
User.add_to_class('location', models.CharField(max_length=100, blank=True))
User.add_to_class('date_of_birth', models.DateField(null=True, blank=True))
User.add_to_class('about', models.TextField(blank=True))

def get_profile_url(self):
    """Returns the URL for this User's profile."""
    return '%s%s/' % (reverse('user', args=[self.id]), self.username)

User.add_to_class('get_profile_url', get_profile_url)

def calculate_gravatar_hash(instance, **kwargs):
    """Calculates a User's gravatar hash from their email address."""
    if kwargs.get('raw', False):
        return
    instance.gravatar = hashlib.md5(instance.email).hexdigest()

pre_save.connect(calculate_gravatar_hash, sender=User)

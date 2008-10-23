import datetime
import random

from django import forms
from django.template.defaultfilters import slugify

from soclone.forms.fields import TagnameField
from soclone.forms.widgets import MarkdownTextArea

RESERVED_TITLES = (u'answer', u'edit', u'delete', u'favourite', u'comment',
                   u'flag', u'vote')

WIKI_CHECKBOX_LABEL = u'community owned wiki question'

def clean_question_title(form):
    """
    Ensures that Question titles don't conflict with URLs used to take
    particular actions on a Question.
    """
    if slugify(form.cleaned_data['title']) in RESERVED_TITLES:
        internets = random.choice([
            u'We have filters on Internets which make',
            u"I hear there's rumors on the, uh, Internets that"])
        raise forms.ValidationError(
            u'%s this title is invalid - please choose another.' % internets)
    return form.cleaned_data['title']

class RevisionForm(forms.Form):
    """
    Lists revisions of a Question or Answer for selection for use as the
    start point for further editing. This isn't included on the relevant
    edit forms because we don't care which revision was selected when the
    edit is being submitted.
    """
    revision = forms.ChoiceField()

    def __init__(self, post, latest_revision, *args, **kwargs):
        super(RevisionForm, self).__init__(*args, **kwargs)
        revisions = post.revisions.all().values_list(
            'revision', 'author__username', 'revised_at', 'summary')
        if (len(revisions) > 1 and
            (revisions[0][2].year == revisions[len(revisions)-1][2].year ==
             datetime.datetime.now().year)):
            # All revisions occured this year, so don't show the revision year
            date_format = '%b %d at %H:%M'
        else:
            date_format = '%b %d %Y at %H:%M'
        self.fields['revision'].choices = [
            (r[0], u'%s - %s (%s) %s' % (r[0], r[1], r[2].strftime(date_format), r[3]))
            for r in revisions]
        self.fields['revision'].initial = latest_revision.revision

class AskQuestionForm(forms.Form):
    title = forms.CharField(max_length=300)
    text  = forms.CharField(widget=MarkdownTextArea())
    tags  = TagnameField()
    wiki  = forms.BooleanField(required=False, label=WIKI_CHECKBOX_LABEL)

    clean_title = clean_question_title

class RetagQuestionForm(forms.Form):
    tags = TagnameField()

    def __init__(self, question, *args, **kwargs):
        super(RetagQuestionForm, self).__init__(*args, **kwargs)
        self.fields['tags'].initial = question.tagnames

class EditQuestionForm(forms.Form):
    title   = forms.CharField(max_length=300)
    text    = forms.CharField(widget=MarkdownTextArea())
    tags    = TagnameField()
    summary = forms.CharField(max_length=300, required=False, label=u'Edit Summary')

    def __init__(self, question, revision, *args, **kwargs):
        """
        Sets the form up to edit the given question, with initial values for
        the given QuestionRevision.
        """
        super(EditQuestionForm, self).__init__(*args, **kwargs)
        self.fields['title'].initial = revision.title
        self.fields['text'].initial = revision.text
        self.fields['tags'].initial = revision.tagnames
        # Once wiki mode is enabled, it can't be disabled
        if not question.wiki:
            self.fields['wiki'] = forms.BooleanField(required=False,
                                                     label=WIKI_CHECKBOX_LABEL)

    clean_title = clean_question_title

class AddAnswerForm(forms.Form):
    text = forms.CharField(widget=MarkdownTextArea())
    wiki = forms.BooleanField(required=False, label=WIKI_CHECKBOX_LABEL)

class EditAnswerForm(forms.Form):
    text    = forms.CharField(widget=MarkdownTextArea())
    summary = forms.CharField(max_length=300, required=False, label=u'Edit Summary')

    def __init__(self, answer, revision, *args, **kwargs):
        """
        Sets the form up to edit the given Answer, with initial values for
        the given AnswerRevision.
        """
        super(EditAnswerForm, self).__init__(*args, **kwargs)
        self.fields['text'].initial = revision.text
        # Once wiki mode is enabled, it can't be disabled
        if not answer.wiki:
            self.fields['wiki'] = forms.BooleanField(required=False,
                                                     label=WIKI_CHECKBOX_LABEL)

class CommentForm(forms.Form):
    comment = forms.CharField(min_length=10, max_length=300, widget=forms.Textarea(attrs={'maxlength': 300, 'cols': 70, 'rows': 2}))

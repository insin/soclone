import re
import urllib

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.defaultfilters import pluralize
from django.utils.safestring import mark_safe

from soclone import auth
from soclone.models import Badge, QUESTIONS_PER_PAGE_CHOICES

register = template.Library()

#############
# Utilities #
#############

extra_params_re = re.compile(r'(\w+)=(".+?"|[\w\.]+)\s*')

def parse_extra_params(contents):
    """
    Input should be 'foo="bar" baz=ter' - output is corresponding dict.
    Raises TemplateSyntaxError if something is wrong with the input.
    """
    unwanted = extra_params_re.sub('', contents)
    if unwanted.strip():
        raise template.TemplateSyntaxError, \
            "Invalid parameter arguments: '%s'" % unwanted.strip()
    return dict(extra_params_re.findall(contents))

def extra_url_params(extra_params, context):
    """
    Generates a URL fragment which specifies any extra parameters given,
    which includes the preceding '&' required to append them to existing
    parameters, or returns an empty string if no extra parameters were
    given.

    Unquoted values in the parameter dict are looked up as variables in
    the given context, while quoted values have their quotes stripped and
    are used as-is.
    """
    if not extra_params:
        return u''
    params = {}
    for param, value in extra_params.iteritems():
        if value[0] == '"' and value[-1] == '"':
            value = value[1:-1]
        else:
            value = template.Variable(value).resolve(context)
        params[param] = value
    return '&amp;%s' % u'&amp;'.join(u'%s=%s' % (urllib.quote_plus(param),
                                                 urllib.quote_plus(value))
                                     for param, value in params.iteritems())

###########
# Filters #
###########

@register.filter
def can_vote_up(user):
    return auth.can_vote_up(user)

@register.filter
def can_flag_offensive(user):
    return auth.can_flag_offensive(user)

@register.filter
def can_add_comments(user):
    return auth.can_add_comments(user)

@register.filter
def can_vote_down(user):
    return auth.can_vote_down(user)

@register.filter
def can_retag_questions(user):
    return auth.can_retag_questions(user)

@register.filter
def can_edit_post(user, post):
    return auth.can_edit_post(user, post)

@register.filter
def can_delete_comment(user, comment):
    return auth.can_delete_comment(user, comment)

@register.filter
def can_close_question(user, question):
    return auth.can_close_question(user, question)

@register.filter
def can_lock_questions(user):
    return auth.can_lock_questions(user)

##################
# Inclusion tags #
##################

@register.inclusion_tag('question_list_user_details.html')
def question_list_user_details(question, view):
    return {
        'question': question,
        'display_user': getattr(question, view.user),
        'display_time': getattr(question, view.time),
        'view': view,
    }

@register.inclusion_tag('post_user_details.html')
def post_user_details(post):
    return {
        'post': post,
        'display_editor': (post.wiki or
                           post.last_edited_by_id != post.author_id),
    }

########
# Tags #
########

GRAVATAR_TEMPLATE = ('<img width="%(size)s" height="%(size)s" '
                     'src="http://www.gravatar.com/avatar/%(gravatar_hash)s'
                     '?s=%(size)s&d=identicon&r=PG">')

@register.simple_tag
def gravatar(user, size):
    """
    Creates an ``<img>`` for a user's Gravatar with a given size.

    This tag can accept a User object, or a dict containing the
    appropriate values.
    """
    try:
        gravatar = user['gravatar']
    except (TypeError, AttributeError, KeyError):
        gravatar = user.gravatar
    return mark_safe(GRAVATAR_TEMPLATE % {
        'size': size,
        'gravatar_hash': gravatar,
    })

REPUTATION_TEMPLATE = '<span class="reputation-score">%s</span>'
BADGE_TEMPLATE = ('<span title="%(count)s %(name)s badge%(plural)s">'
                    '<span class="badge%(id)s">&bull;</span>'
                    '<span class="badgecount">%(count)s</span>'
                  '</span>')

@register.simple_tag
def reputation(user):
    """
    Creates a ``<span>`` for a User's reputation score and for each type
    of badge they hold.

    This tag can accept a User object, or a dict containing the
    appropriate values.
    """
    try:
        reputation, gold, silver, bronze = (user['reputation'], user['gold'],
                                            user['silver'], user['bronze'])
    except (TypeError, AttributeError, KeyError):
        reputation, gold, silver, bronze = (user.reputation, user.gold,
                                            user.silver, user.bronze)
    spans = [REPUTATION_TEMPLATE % intcomma(reputation)]
    for badge, count in zip(Badge.TYPE_CHOICES, (gold, silver, bronze)):
        if not count:
            continue
        spans.append(BADGE_TEMPLATE % {
            'id': badge[0],
            'name': badge[1],
            'count': count,
            'plural': pluralize(count),
        })
    return mark_safe(u''.join(spans))

class PagerNode(template.Node):
    def __init__(self, page_var, extra_params):
        self.page_var = template.Variable(page_var)
        self.extra_params = extra_params

    def render(self, context):
        page = self.page_var.resolve(context)
        link_template = (u'<a href="?page=%%s%s" class="%%s">%%s</a>' %
                         extra_url_params(self.extra_params, context))
        html = [u'<div class="pager">']
        if page.has_previous():
            html.append(link_template % (page.previous_page_number(),
                                         u'previous', u'previous'))
        if page.number > 2:
            html.append(link_template % (1, u'first page-number', 1))
            if page.number > 3:
                html.append(u'<span class="divider">&hellip;</span>')
        if page.has_previous():
            html.append(link_template % (page.previous_page_number(),
                                         u'page-number',
                                         page.previous_page_number()))
        html.append(u'<span class="current page-number">%s</span>' % page.number)
        if page.has_next():
            html.append(link_template % (page.next_page_number(),
                                         u'page-number',
                                         page.next_page_number()))
        if page.number < page.paginator.num_pages - 1:
            if page.number < page.paginator.num_pages - 2:
                html.append(u'<span class="divider">&hellip;</span>')
            html.append(link_template % (page.paginator.num_pages,
                                         u'last page-number',
                                         page.paginator.num_pages))
        if page.has_next():
            html.append(link_template % (page.next_page_number(), u'next',
                                         u'next'))
        html.append(u'</div>')
        return u' '.join(html)

@register.tag(name='pager')
def do_pager(parser, token):
    # Can't use split_contents here as we need to process 'sort="foo"' etc
    bits = token.contents.split()
    if len(bits) == 1:
        raise template.TemplateSyntaxError, \
            "%r tag takes arguments" % bits[0]
    page_var = bits[1]
    extra_params = {}
    if len(bits) > 2:
        # There are extra param=value arguments to consume
        extra_params = parse_extra_params(' '.join(bits[2:]))
    return PagerNode(page_var, extra_params)

class SizerNode(template.Node):
    def __init__(self, page_var, extra_params):
        self.page_var = template.Variable(page_var)
        self.extra_params = extra_params

    def render(self, context):
        page = self.page_var.resolve(context)
        link_template = (
            u'<a href="?page=%s&amp;pagesize=%%s%s" class="%%s">%%s</a>' % (
                page.number, extra_url_params(self.extra_params, context)))
        html = [u'<div class="sizer">']
        for page_size, description in QUESTIONS_PER_PAGE_CHOICES:
            if page.paginator.per_page == page_size:
                class_ = u'current page-number'
            else:
                class_ = u'page-number'
            html.append(link_template % (page_size, class_, page_size))
        html.append(u'<span class="per-page">per page</span>')
        html.append(u'</div>')
        return u' '.join(html)

@register.tag(name='sizer')
def do_sizer(parser, token):
    # Can't use split_contents here as we need to process 'sort="foo"' etc
    bits = token.contents.split()
    if len(bits) == 1:
        raise template.TemplateSyntaxError, \
            "%r tag takes arguments" % bits[0]
    page_var = bits[1]
    extra_params = {}
    if len(bits) > 2:
        # There are extra param=value arguments to consume
        extra_params = parse_extra_params(' '.join(bits[2:]))
    return SizerNode(page_var, extra_params)

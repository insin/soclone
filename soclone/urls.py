from django.conf import settings
from django.conf.urls.defaults import *

from soclone.models import Answer, Question

urlpatterns = patterns('soclone.views',
    url(r'^$',                                           'index',              name='index'),
    url(r'^about/$',                                     'about',              name='about'),
    url(r'^faq/$',                                       'faq',                name='faq'),
    url(r'^search/$',                                    'search',             name='search'),
    url(r'^login/$',                                     'login',              name='login'),
    url(r'^logout/$',                                    'logout',             name='logout'),
    url(r'^questions/$',                                 'questions',          name='questions'),
    url(r'^questions/ask/$',                             'ask_question',       name='ask_question'),
    url(r'^questions/tagged/(?P<tag_name>[^/]+)/$',      'tag',                name='tag'),
    url(r'^questions/(?P<question_id>\d+)/answer/$',     'add_answer',         name='add_answer'),
    url(r'^questions/(?P<question_id>\d+)/close/$',      'close_question',     name='close_question'),
    url(r'^questions/(?P<question_id>\d+)/edit/$',       'edit_question',      name='edit_question'),
    url(r'^questions/(?P<question_id>\d+)/delete/$',     'delete_question',    name='delete_question'),
    url(r'^questions/(?P<question_id>\d+)/favourite/$',  'favourite_question', name='favourite_question'),
    url(r'^questions/(?P<question_id>\d+)/revisions/$',  'question_revisions', name='question_revisions'),
    url(r'^questions/(?P<object_id>\d+)/comment/$',      'add_comment',        name='add_question_comment', kwargs={'model': Question}),
    url(r'^questions/(?P<object_id>\d+)/flag/$',         'flag_item',          name='flag_question', kwargs={'model': Question}),
    url(r'^questions/(?P<object_id>\d+)/vote/$',         'vote',               name='vote_on_question', kwargs={'model': Question}),
    url(r'^questions/(?P<question_id>\d+)/(?:[^/]+/)?$', 'question',           name='question'),
    url(r'^unanswered/$',                                'unanswered',         name='unanswered'),
    url(r'^answers/(?P<answer_id>\d+)/$',                'answer_comments',    name='answer'),
    url(r'^answers/(?P<answer_id>\d+)/edit/$',           'edit_answer',        name='edit_answer'),
    url(r'^answers/(?P<answer_id>\d+)/revisions/$',      'answer_revisions',   name='answer_revisions'),
    url(r'^answers/(?P<object_id>\d+)/comment/$',        'add_comment',        name='add_answer_comment', kwargs={'model': Answer}),
    url(r'^answers/(?P<object_id>\d+)/flag/$',           'flag_item',          name='flag_answer', kwargs={'model': Answer}),
    url(r'^answers/(?P<object_id>\d+)/vote/$',           'vote',               name='vote_on_answer', kwargs={'model': Answer}),
    url(r'^comments/(?P<comment_id>\d+)/delete/$',       'delete_comment',     name='delete_comment'),
    url(r'^tags/$',                                      'tags',               name='tags'),
    url(r'^users/$',                                     'users',              name='users'),
    url(r'^users/(?P<user_id>\d+)/(?:[^/]+/)?$',         'user',               name='user'),
    url(r'^badges/$',                                    'badges',             name='badges'),
    url(r'^badges/(?P<badge_id>\d+)/(?:[^/]+/)?$',       'badge',              name='badge'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

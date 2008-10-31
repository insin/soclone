from soclone.models import Question

class QuestionView(object):
    """A view of the list of Questions."""
    def __init__(self, id=None, page_title=None, tab_title=None,
                 tab_tooltip=None, description=None,  user='author',
                 user_action='asked',
                 user_fields=('username', 'gravatar', 'reputation',
                                      'gold', 'silver', 'bronze'),
                 time='added_at'):
        self.id = id
        self.page_title = page_title
        self.tab_title = tab_title
        self.tab_tooltip = tab_tooltip
        self.description = description
        self.user = user
        self.user_action = user_action
        self.user_fields = user_fields
        self.time = time

    def get_queryset(self):
        raise NotImplementedError

class OrderedQuestionView(QuestionView):
    """A view in which list of Questions has a simple order applied."""
    def __init__(self, ordering=None, **kwargs):
        if ordering is None:
            ordering = ()
        self.ordering = ordering
        super(OrderedQuestionView, self).__init__(**kwargs)

    def get_queryset(self):
        return Question.objects.all().order_by(*self.ordering)

class HotQuestionView(QuestionView):
    """
    A question view which applies a "hotness" algorithm to sort all
    Questions.
    """
    def get_queryset(self):
        raise NotImplementedError

all_question_views = (
    OrderedQuestionView(
        id          = 'newest',
        page_title  = 'Newest Questions',
        tab_title   = 'Newest',
        tab_tooltip = 'The most recently asked questions',
        description = 'sorted by the <strong>date they were asked</strong>. '
                      'The newest, most recently asked questions will appear '
                      'first',
        ordering    = ('-added_at',)
    ),
    HotQuestionView(
        id          = 'hot',
        page_title  = 'Hottest Questions',
        tab_title   = 'Hot',
        tab_tooltip = 'Questions with recent interest and activity',
        description = 'sorted by <strong>hotness</strong>. Questions with the '
                      'most recent interest and activity will appear first.'
    ),
    OrderedQuestionView(
        id          = 'votes',
        page_title  = 'Highest Voted Questions',
        tab_title   = 'Votes',
        tab_tooltip = 'Questions with the most votes',
        description = 'sorted by <strong>votes</strong>. The questions with '
                      ' the highest vote scores (up votes minus down votes) '
                      'will appear first.',
        ordering    = ('-score', '-added_at'),
    ),
    OrderedQuestionView(
        id           = 'activity',
        page_title   = 'Recently Active Questions',
        tab_title    = 'Activity',
        tab_tooltip  = 'Questions that have recent activity',
        description  = 'sorted by <strong>activity</strong>. Questions with '
                       'the most recent activity &mdash; either through new '
                       'answers or recent edits &mdash; will appear first.',
        ordering     = ('-last_activity_at',),
        user         = 'last_activity_by',
        user_action  = 'modified',
        time         = 'last_activity_at'
    )
)

# TODO Implement unanswered views
unanswered_question_views = all_question_views

# TODO Implement index views
index_question_views = all_question_views

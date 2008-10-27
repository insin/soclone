"""
Authorisation related functions.

The actions a User is authorised to perform are dependent on their reputation
and superuser status.
"""
VOTE_UP = 15
FLAG_OFFENSIVE = 15
LEAVE_COMMENTS = 50
VOTE_DOWN = 100
CLOSE_OWN_QUESTIONS = 250
RETAG_OTHER_QUESTIONS = 500
EDIT_COMMUNITY_WIKI_POSTS = 750
EDIT_OTHER_POSTS = 2000
DELETE_COMMENTS = 2000
CLOSE_OTHER_QUESTIONS = 3000
LOCK_QUESTIONS = 4000

def can_vote_up(user):
    """Determines if a User can vote Questions and Answers up."""
    return user.is_authenticated() and (
        user.reputation >= VOTE_UP or
        user.is_superuser)

def can_flag_offensive(user):
    """Determines if a User can flag Questions and Answers as offensive."""
    return user.is_authenticated() and (
        user.reputation >= FLAG_OFFENSIVE or
        user.is_superuser)

def can_add_comments(user):
    """Determines if a User can add comments to Questions and Answers."""
    return user.is_authenticated() and (
        user.reputation >= LEAVE_COMMENTS or
        user.is_superuser)

def can_vote_down(user):
    """Determines if a User can vote Questions and Answers down."""
    return user.is_authenticated() and (
        user.reputation >= VOTE_DOWN or
        user.is_superuser)

def can_retag_questions(user):
    """Determines if a User can retag Questions."""
    return user.is_authenticated() and (
        RETAG_OTHER_QUESTIONS <= user.reputation < EDIT_OTHER_POSTS)

def can_edit_post(user, post):
    """Determines if a User can edit the given Question or Answer."""
    return user.is_authenticated() and (
        user.id == post.author_id or
        (post.wiki and user.reputation >= EDIT_COMMUNITY_WIKI_POSTS) or
        user.reputation >= EDIT_OTHER_POSTS or
        user.is_superuser)

def can_delete_comment(user, comment):
    """Determines if a User can delete the given Comment."""
    return user.is_authenticated() and (
        user.id == comment.user_id or
        user.reputation >= DELETE_COMMENTS or
        user.is_superuser)

def can_close_question(user, question):
    """Determines if a User can close the given Question."""
    return user.is_authenticated() and (
        (user.id == question.author_id and
         user.reputation >= CLOSE_OWN_QUESTIONS) or
        user.reputation >= CLOSE_OTHER_QUESTIONS or
        user.is_superuser)

def can_lock_questions(user):
    """Determines if a User can lock Questions."""
    return user.is_authenticated() and (
        user.reputation >= LOCK_QUESTIONS or
        user.is_superuser)

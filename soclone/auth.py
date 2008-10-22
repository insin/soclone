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
LOCK_OTHER_QUESTIONS = 4000

def can_retag_questions(user):
    """Determines if a user can retag any Question."""
    return user.is_authenticated() and (
               RETAG_OTHER_QUESTIONS <= user.reputation < EDIT_OTHER_POSTS)

def can_edit_post(user, post):
    """Determines if a user can edit the given Question or Answer."""
    return user.is_authenticated() and (
               user.id == post.author_id or
               user.reputation >= EDIT_OTHER_POSTS or
               user.is_superuser)

def can_close_question(user, question):
    """Determines if a user can close a given Question."""
    return user.is_authenticated() and (
               user.id == question.author_id or
               user.reputation >= CLOSE_OTHER_QUESTIONS or
               user.is_superuser)

def can_delete_comment(user, comment):
    """Determines if a user can delete the given Comment."""
    return user.is_authenticated() and (
               user.id == comment.user_id or
               user.reputation >= DELETE_COMMENTS or
               user.is_superuser)

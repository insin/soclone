def auth(request):
    """
    A modified version of django.core.context_processors.auth which
    doesn't use Messages or Permissions.
    """
    if hasattr(request, 'user'):
        user = request.user
    else:
        from django.contrib.auth.models import AnonymousUser
        user = AnonymousUser()
    return {
        'user': user,
    }

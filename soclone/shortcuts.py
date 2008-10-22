from django.core.paginator import EmptyPage

def get_page(request, paginator, page_param='page'):
    """
    Uses the page number specified as a GET parameter in a request to
    retrieve a page of objects from a paginator.

    If a page number isn't specified or isn't a valid integer value, the
    first page will be retrieved.

    If the specified page is empty, the last page will be retrieved.
    """
    try:
        page = int(request.GET.get(page_param, '1'))
    except ValueError:
        page = 1

    try:
        return paginator.page(page)
    except EmptyPage:
        return paginator.page(paginator.num_pages)

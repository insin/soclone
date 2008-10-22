"""Template tags for working with lists of items."""
from django import template

register = template.Library()

@register.filter
def in_batches_of_size(items, size):
    """
    Retrieves items in batches of the given size.

    >>> l = range(1, 11)
    >>> in_batches_of_size(l, 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
    >>> in_batches_of_size(l, 5)
    [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
    """
    size = int(size)
    return [items[i:i+size] for i in xrange(0, len(items), size)]

@register.filter
def in_batches(items, batches):
    """
    Retrieves items in the given number of batches.

    >>> l = range(1, 11)
    >>> in_batches(l, 1)
    [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
    >>> in_batches(l, 2)
    [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
    >>> in_batches(l, 3)
    [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10]]
    >>> in_batches(l, 4)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
    >>> in_batches(l, 5)
    [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]
    >>> in_batches(l, 6)
    [[1, 2], [3, 4], [5, 6], [7, 8], [9], [10]]
    >>> in_batches(l, 7)
    [[1, 2], [3, 4], [5, 6], [7], [8], [9], [10]]
    >>> in_batches(l, 8)
    [[1, 2], [3, 4], [5], [6], [7], [8], [9], [10]]
    >>> in_batches(l, 9)
    [[1, 2], [3], [4], [5], [6], [7], [8], [9], [10]]
    >>> in_batches(l, 10)
    [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
    >>> in_batches(l, 11)
    [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], []]
    """
    batches = int(batches)
    div, mod= divmod(len(items), batches)
    if div > 1:
        if mod:
            div += 1
        return in_batches_of_size(items, div)
    else:
        if not div:
            return [[item] for item in items] + [[]] * (batches - mod)
        elif div == 1 and not mod:
            return [[item] for item in items]
        else:
            # mod now tells you how many lists of 2 you can fir in
            return ([items[i*2:(i*2)+2] for i in xrange(0, mod)] +
                    [[item] for item in items[mod*2:]])

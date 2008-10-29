"""Template tags for working with lists of items."""
from django import template

from soclone.utils.lists import batch_size, batches

register = template.Library()

@register.filter
def in_batches_of_size(items, size):
    """
    Retrieves items in batches of the given size.
    """
    return batch_size(items, int(size))

@register.filter
def in_batches(items, number):
    """
    Retrieves items in the given number of batches.
    """
    return batches(items, int(number))

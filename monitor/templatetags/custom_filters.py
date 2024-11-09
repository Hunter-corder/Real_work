from django import template

register = template.Library()

@register.filter
def get_item(value, arg):
    """Retrieve an item from a list by index."""
    try:
        return value[int(arg)]
    except (IndexError, ValueError):
        return None

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a key."""
    if isinstance(dictionary, dict):
        value = dictionary.get(key, '')
        # Round floats to 4 decimal places if they are numeric
        if isinstance(value, float):
            return round(value, 4)
        return value
    return ''

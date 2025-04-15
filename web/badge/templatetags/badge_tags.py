from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a key"""
    return dictionary.get(key)

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    return value * arg

@register.filter
def divide(value, arg):
    """Divide the value by the argument"""
    if arg == 0:
        return 0
    return value / arg

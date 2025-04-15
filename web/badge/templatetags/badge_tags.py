# In badge/templatetags/badge_tags.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a variable key"""
    return dictionary.get(key)

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    """Divide the value by the argument"""
    try:
        arg = float(arg)
        if arg == 0:
            return 0
        return float(value) / arg
    except (ValueError, TypeError):
        return 0

@register.simple_tag
def badge_progress_percent(progress, badge):
    """Calculate percentage progress toward a badge"""
    if not progress or not badge.requirement_count:
        return 0
    
    percent = (progress / badge.requirement_count) * 100
    # Cap at 100%
    return min(percent, 100)

@register.filter
def badge_color(category):
    """Return the appropriate badge color based on category"""
    colors = {
        'participant': 'primary',
        'helper': 'info',
        'organizer': 'success'
    }
    return colors.get(category, 'secondary')

@register.filter
def badge_level_color(level):
    """Return the appropriate color for badge level"""
    colors = {
        1: 'warning',
        2: 'info',
        3: 'primary',
        4: 'danger'
    }
    return colors.get(level, 'secondary')

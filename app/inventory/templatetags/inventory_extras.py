# EntrataMerci/app/inventory/templatetags/inventory_extras.py
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def replace_char(value, arg):
    """Replaces all occurrences of arg from string with replace_with."""
    if len(arg) != 2: # Aspetta una stringa tipo "-_" o " _"
        return value 
    char_to_replace = arg[0]
    replace_with = arg[1]
    return value.replace(char_to_replace, replace_with)

from django import template
import re

register = template.Library()

@register.filter
def remove_page(value):
    replace_value = re.sub(r"$page=(\d+)", '', value)
    # replace_value = re.sub(r"\$page=(\d+)", '', value)
    return replace_value

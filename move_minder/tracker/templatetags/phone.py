from django import template
from phonenumber_field import phonenumber

register = template.Library()

@register.filter
def phone(value):
    if value is not None and value != "":
        return value.as_national
    else:
        return value
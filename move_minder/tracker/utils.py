from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def validate_postal_code(value):
    us = re.compile(r'^\d{5}$')
    can = re.compile(r'^[a-zA-Z]{1}\d{1}[a-zA-Z]{1} \d{1}[a-zA-Z]{1}\d{1}$')

    is_us = us.match(value)
    is_can = can.match(value)

    if is_us is None and is_can is None:
        raise ValidationError(_("%(value)s is not a valid postal code"), params={"value": value})
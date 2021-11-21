
from django.core.exceptions import ValidationError


def validate_name(name):
    from .models import Register
    match = Register.objects.filter(name=name)
    if name in match:
        raise ValidationError('This name is already in use')
    return match

        
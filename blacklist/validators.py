import re
from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError


cpf_error_messages = {
    'invalid': "CPF Inválido.",
    'digits_only': "Somente é permitido números.",
    'max_digits': "Este campo requer 11 dígitos",
}


def dv_maker(v):
    if v >= 2:
        return 11 - v
    return 0


def validate_CPF(value):
    """
    Value can be either a string in the format XXX.XXX.XXX-XX or an
    11-digit number.
    """

    if value in EMPTY_VALUES:
        return u''
    if not value.isdigit():
        value = re.sub("[-\.]", "", value)
    orig_value = value[:]
    try:
        int(value)
    except ValueError:
        raise ValidationError(cpf_error_messages['digits_only'])
    if len(value) != 11:
        raise ValidationError(cpf_error_messages['max_digits'])
    orig_dv = value[-2:]

    new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(10, 1, -1))])
    new_1dv = dv_maker(new_1dv % 11)
    value = value[:-2] + str(new_1dv) + value[-1]
    new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(11, 1, -1))])
    new_2dv = dv_maker(new_2dv % 11)
    value = value[:-1] + str(new_2dv)
    if value[-2:] != orig_dv:
        raise ValidationError(cpf_error_messages['invalid'])

    return orig_value

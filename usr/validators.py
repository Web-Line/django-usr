from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


def national_id_validator(value):
    """
    Check if national_id is correct.
    :param value: national_id
    :type value: str
    :raises: ValidationError
    :returns: None
    """
    # We don't need validation when DEBUG is True.
    if settings.DEBUG:
        return

    if len(value) != 10:
        raise ValidationError(_('National ID most contain exactly 10 digits'))

    numbers_list = []
    result = 0
    for chars in value:
        try:
            numbers_list.append(int(chars))
        except:
            raise ValidationError(_('National ID must be numeric'))

    numbers_list = list(reversed(numbers_list))
    for i in range(len(numbers_list)):
        if i != 0:
            result += (i + 1) * numbers_list[i]

    if result % 11 < 2:
        control = result % 11
    else:
        control = 11 - (result % 11)
    if control != numbers_list[0]:
        raise ValidationError(_('Invalid National ID, Please make sure provided'
                                ' National ID is correct'))

#  Copyright (c) 2020
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_course_level(value):
    # Validate course level
    valid_state = {'Beginer': True, 'Intermediate': True, 'Advance': True}
    if valid_state.get(value) is None:
        raise ValidationError(
            _('%(value)s is not a valid level'),
            params={'value': value},
        )


def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls', '.zip', '.rar', '.ppt']
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Unsupported file extension.'))

import os

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.doc', '.docx', '.odt', '.rtf', '.jpg', '.jpeg', '.png', '.tif', '.tiff']
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Unsupported file extension.'))

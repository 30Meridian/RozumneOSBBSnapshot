from django import forms
from django.utils.translation import ugettext as _

from system.models import Condominium


class CondominiumUpdateForm(forms.ModelForm):
    slug = forms.SlugField(label=_('slug'))

    class Meta:
        model = Condominium
        fields = ['name', 'legal_address', 'ideas_days', 'votes', 'problem_days',]

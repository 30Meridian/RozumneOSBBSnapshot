from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_slug

from .models import Category

from unidecode import unidecode
from re import match


class ArticlesAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticlesAdminForm, self).__init__(*args, **kwargs)
        self.fields['datetime_publish'].help_text = _('Enter date and time if you want to make deferred publication')
        self.fields['datetime_publish'].required = False
        # self.fields['public'].initial = self.current_condominium.public_news


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']

    def clean(self):
        cleaned_data = super(AddCategoryForm, self).clean()
        title = cleaned_data.get('title')
        if match("^[\w ]+$", title):
            return cleaned_data
        else:
            raise forms.ValidationError(_('Name should consist of letters, numbers, underscores and spaces'))


class UpdateCategoryForm(forms.ModelForm):
    class Meta:
        fields = ['title', 'slug']

    def clean(self):
        cleaned_data = super(UpdateCategoryForm, self).clean()
        title = cleaned_data.get('title')
        slug = unidecode(cleaned_data.get('slug'))

        if not match("^[\w ]+$", title):
            raise forms.ValidationError(_('Name should consist of letters, numbers, underscores and spaces'))

        try:
            validate_slug(slug)
        except forms.ValidationError:
            raise forms.ValidationError(_('Slug should consist of letters, numbers, underscores and dashes '))

        return cleaned_data

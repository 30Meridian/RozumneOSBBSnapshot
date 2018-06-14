from django import forms
from django.utils.translation import ugettext_lazy as _

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Pages


class PageCreate(forms.ModelForm):
    class Meta:
        model = Pages
        fields = ['slug', 'title', 'content']
        widgets = {
            'slug': forms.TextInput(attrs={'placeholder': _('Page address.No more than 64 characters'),
                                           'class': 'form-control input-lg'}),
            'title': forms.TextInput(attrs={'placeholder': _('Page title. No more than 128 characters.'),
                                            'class': 'form-control input-lg'}),
            'content': CKEditorUploadingWidget
        }

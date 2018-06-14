from .models import Items
from django import forms
from django.utils.translation import ugettext_lazy as _

class ItemsCreate(forms.ModelForm):
    class Meta:
        model = Items
        fields = ['title', 'description', 'photo', 'public']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':
                                                _('Please, enter short item title. Not more than 255 characters'),
                                            'class': 'form-control input-lg'}, ),
            'description': forms.Textarea(attrs={'placeholder':
                                                     _('Detailed description of the item. No more than 3,000 characters.'),
                                                 'class': 'form-control input-lg',
                                                 'style': 'resize: none;'}),
            'photo': forms.FileInput(attrs={'class': "filestyle", 'data-buttonText': _('Choose picture'),
                                            'data-badge': "false", 'data-buttonBefore': "true"}),
            # 'public': forms.CheckboxInput(attrs={'class': "public-problem", 'style': ''}),
        }

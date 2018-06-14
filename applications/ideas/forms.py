from ideas.models import Ideas
from django import forms
from django.utils.translation import ugettext_lazy as _

class IdeaAdd(forms.ModelForm):
    class Meta:
        model = Ideas
        fields = ['title','image', 'text', 'anonymous', 'public']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('Enter idea title'),
                                            'class': 'form-control input-lg'}),
            'text': forms.Textarea(attrs={'placeholder': _('Please enter description of raised idea and give arguments '
                                                           'why this idea should be satisfied (max: 1000 characters)'),
                                          'class': 'form-control input-lg',
                                          'rows': 10, 'cols': 64, 'style': 'resize: none;'}),
            'image': forms.FileInput(attrs={'class':"filestyle",'data-buttonText': _("Choose picture"),
                                            'data-badge':"false",'data-buttonBefore':"true"}),
        }


# class IdeaChangeStatus(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(IdeaChangeStatus, self).__init__(*args, **kwargs)
#         self.fields['resolution'].required = True
#         self.fields['resolution'].label = False
#
#     class Meta:
#         model = Ideas
#         fields = ['resolution']
#         widgets = {
#                 'resolution': forms.Textarea(attrs={'placeholder': 'Опишіть причину зміни статусу: порушення, виконання робіт, тощо... ', 'class': 'form-control input-lg',}),
#         }

class IdeaAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(IdeaAdminForm, self).__init__(*args, **kwargs)
        # self.fields['public'].initial = self.current_condominium.public_ideas

    text = forms.CharField(max_length=2000,
                           widget=forms.Textarea(attrs={'rows': 15, 'style': 'resize: none; width: 90%'}), label=_('idea text'))
    resolution = forms.CharField(max_length=2000, required=False,
                                 widget=forms.Textarea(attrs={'rows': 15, 'style': 'resize: none; width: 90%'}), label=_('idea resolution'))



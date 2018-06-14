from news.models import News
from django import forms
from django.utils.translation import ugettext_lazy as _
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# class NewsAdd(forms.ModelForm):
#     class Meta:
#         model = News
#         fields = ['title','shortdesc','text', 'mainimg', 'publish']
#         widgets = {
#             'title': forms.TextInput(attrs={'placeholder': 'Уведіть заголовок новини. Не більше 150 символів', 'class': 'form-control input-lg'}, ),
#             'shortdesc': forms.Textarea(attrs={'placeholder': 'Короткий текст, що передає контекст новини. Не більше 300 символів.', 'class': 'form-control input-lg',}),
#             'text': CKEditorUploadingWidget(),
#             'mainimg': forms.FileInput(attrs={'class':"filestyle",'data-buttonText': "Виберіть зображення", 'data-badge':"false",'data-buttonBefore':"true"}),
#
#         }

class NewsAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewsAdminForm, self).__init__(*args, **kwargs)
        self.fields['datetime_publish'].help_text = _('Enter date and time if you want to make deferred publication')
        self.fields['datetime_publish'].required = False
        # self.fields['public'].initial = self.current_condominium.public_news
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.core.exceptions import ValidationError

from system.models import User, Condominium
from polls.models import Poll, Choice, Vote

class ChoiseInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(ChoiseInlineFormSet, self).clean()
        image_list = []
        choice_list = []
        for form in self.forms:
            if form.cleaned_data:
                if form.cleaned_data['image']:
                    image_list.append(form.cleaned_data['image'])
                if form.cleaned_data['choice']:
                    choice_list.append(form.cleaned_data['choice'])

        if not (choice_list or image_list):
            raise ValidationError(_('Please add some choices or images'))
        if choice_list and image_list:
            raise ValidationError(_('Please add pictures or choices, but not both!'))


class ChoiceInline(admin.TabularInline):
    formset = ChoiseInlineFormSet
    verbose_name_plural = _("Choices of poll (Please add only pictures or only text).")
    model = Choice
    min_num = 1
    extra = 0
    max_num = 25


class PollAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PollAdminForm, self).__init__(*args, **kwargs)
        # self.fields['public'].initial = self.current_condominium.public_polls
    description = forms.CharField(max_length=2000,
                          widget=forms.Textarea(attrs={'rows': 15, 'style': 'resize: none; width: 90%'}), label = _('description'))


class PollAdmin(admin.ModelAdmin):
    model = Poll
    form = PollAdminForm
    inlines = (ChoiceInline,)
    list_display = ('question', 'count_choices',
                    'count_total_votes', 'date_start',
                    'date_end', 'archive', 'active',
                    'public')
    exclude = ('author', 'condominium')

    def get_form(self, request, obj=None, **kwargs):
        form = super(PollAdmin, self).get_form(request, obj, **kwargs)
        form.current_condominium = Condominium.objects.get(id=request.session['condominium_id'])
        return form

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.condominium = Condominium.objects.get(slug=request.session['condominium_slug'])
        obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(PollAdmin, self).get_queryset(request)
        else:
            qs = super(PollAdmin, self).get_queryset(request)
            return qs.filter(condominium=request.session['condominium_id'])

admin.site.register(Poll, PollAdmin)

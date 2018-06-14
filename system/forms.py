import string
import re
import json

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from django.contrib.auth.models import Group
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from unidecode import unidecode
from haystack.forms import ModelSearchForm

from .models import Condominium, CondominiumNonResidentialPremise, CondominiumResidentialPremise, CondominiumPosition, \
    City, ObjectTypes, CondominiumFloor, User, CondominiumPorch, CondominiumHouse


class SignupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    error_css_class = 'myerror'
    required_css_class = 'myrequired'

    class Meta:
        model = get_user_model()
        fields = ('last_name', 'first_name', 'middle_name', 'phone', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': _('Please enter name, for example: Eugene'),
                                                 'class': 'form-control input-lg'}),
            'last_name': forms.TextInput(attrs={'placeholder': _('Please enter last name, for example: Poremchuk'),
                                                'class': 'form-control input-lg'}),
            'middle_name': forms.TextInput(attrs={'placeholder': _('Please enter middle name, fro example: Volodymyrovych'),
                                                  'class': 'form-control input-lg'}),
            'phone': forms.TextInput(attrs={'placeholder': _('Please enter your phone, for example: 097 111 22 33'),
                                            'class': 'form-control input-lg'}),
        }

    def signup(self, request, user):
        try:
            user.first_name = string.capwords(self.cleaned_data['first_name'].lower())
            user.middle_name = string.capwords(self.cleaned_data['middle_name'].lower())
            user.last_name = string.capwords(self.cleaned_data['last_name'].lower())
            user.phone = self.cleaned_data['phone']
            user.save()

            user.groups.add(Group.objects.get(name='user'))

        except Exception as e:
            raise e


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True
        self.fields['phone'].required = True

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'middle_name', 'phone']


class LocalizedSelect(forms.Select):
    def render_option(self, selected_choices, option_value, option_label):
        return super(LocalizedSelect, self).render_option(selected_choices, option_value, _(option_label))


class ResidentialPremiseAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        condominiums = kwargs.pop('condominiums')
        super(ResidentialPremiseAddForm, self).__init__(*args, **kwargs)
        self.fields['floor'].queryset = CondominiumFloor.objects.filter(
            porch__house__condominium__in=condominiums).all()
        self.fields['type'].queryset = ObjectTypes.objects.filter(category='CondominiumResidentialPremise')

    def save(self, commit=True):
        return super(ResidentialPremiseAddForm, self).save(commit=False)

    class Meta:
        model = CondominiumResidentialPremise
        fields = ['number', 'area', 'residential_area', 'heating_area', 'rooms_count', 'residents_count', 'pets_count',
                  'floor', 'type', 'description']
        widgets = {
            'number': forms.TextInput(),
            'area': forms.NumberInput(attrs={'min': '0.01', 'step': '0.01'}),
            'residential_area': forms.NumberInput(attrs={'min': '0.01', 'step': '0.01'}),
            'heating_area': forms.NumberInput(attrs={'min': '0.01', 'step': '0.01'}),
            'rooms_count': forms.NumberInput(attrs={'min': '1'}),
            'residents_count': forms.NumberInput(attrs={'min': '1'}),
            'pets_count': forms.NumberInput(attrs={'min': '0'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 64, 'style': 'resize: none;'}),
            'floor': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true', }),
            'type': LocalizedSelect(attrs={'class': 'selectpicker'})
        }


class NonResidentialPremiseAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        condominiums = kwargs.pop('condominiums')
        super(NonResidentialPremiseAddForm, self).__init__(*args, **kwargs)
        self.fields['floor'].queryset = CondominiumFloor.objects.filter(
            porch__house__condominium__in=condominiums).all()
        self.fields['type'].queryset = ObjectTypes.objects.filter(category='CondominiumNonResidentialPremise')

    def save(self, commit=True):
        return super(NonResidentialPremiseAddForm, self).save(commit=False)

    class Meta:
        model = CondominiumNonResidentialPremise
        fields = ['number', 'area', 'floor', 'type', 'description']
        widgets = {
            'number': forms.TextInput(),
            'area': forms.NumberInput(attrs={'min': '0.01', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 64, 'style': 'resize: none;'}),
            'floor': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true', }),
            'type': LocalizedSelect(attrs={'class': 'selectpicker'})
        }


class CityChoiceField(forms.ChoiceField):
    def clean(self, value):
        try:
            return City.objects.get(pk=value)
        except:
            if self.required:
                raise forms.ValidationError(message=_('This field is required.'))
            else:
                return None


class CondominiumChoiceField(forms.CharField):
    def clean(self, value):
        try:
            return Condominium.objects.get(pk=value)
        except:
            if self.required:
                raise forms.ValidationError(message=_('This field is required.'))
            else:
                return None


class CondominiumCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CondominiumCreateForm, self).__init__(*args, **kwargs)
        if 'city' in self.changed_data:
            city_query = City.objects.filter(id=self.data[(self.prefix + '-' if self.prefix else '') + 'city'])
            if city_query.count() == 1:
                city = city_query.first()
                self.fields['city'].choices = [(city.id, str(city))]

    city = CityChoiceField(label=_('City'), widget=forms.Select(attrs={
        'title': _('Chose your city. Use search to find more.'),
        'class': 'selectpicker',
        'data-live-search': 'true'
    }))
    position = forms.ChoiceField(label=_('Position'), widget=forms.Select(attrs={
        'title': _('Chose one of the following'),
        'class': 'selectpicker',
    }), choices=CondominiumPosition.POSITIONS)
    checkbox = forms.BooleanField(label=_('I read system rules and consent to the processing of personal data.'),
                                  widget=forms.CheckboxInput(attrs={}),
                                  required=True)

    def save(self, commit=True):
        instance = super(CondominiumCreateForm, self).save(commit=False)

        decoded = unidecode(instance.name)
        allow = string.digits + string.ascii_letters + '-_'
        slug = re.sub('[^%s]' % allow, '', decoded).lower()[:52]
        if len(slug) == 0:
            slug = 'slug'
        instance.slug = slug

        i = 0
        while True:
            if Condominium.objects.filter(slug=instance.slug).count():
                i += 1
                instance.slug = slug + str(i)
            else:
                instance.save()
                break
        return instance

    class Meta:
        model = Condominium
        fields = ['city', 'name', 'legal_address', 'position', 'public_ideas', 'public_news', 'public_polls', 'public_problems', 'checkbox', 'latitude', 'longitude']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': _('Condominium name')}),
            'legal_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Write condominium legal address')
            }),
        }


class DisplayCondominiumsTable(forms.Widget):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        table_attrs = final_attrs.copy()
        table_attrs['id'] += '_table'
        output = [format_html('<table{} class="table">', flatatt(table_attrs))]
        table_head = self.render_head()
        if table_head:
            output.append(table_head)
        table_body = self.render_table_body(value)
        if table_body:
            output.append(table_body)
        output.append('</table>')
        output.append(format_html('<input {} value="{}" type="hidden">', flatatt(final_attrs), value))
        return mark_safe('\n'.join(output))

    def render_head(self):
        output = []
        output.append('<thead><tr>')
        output.append('<th>' + _('Name') + '</th>')
        output.append('<th class="text-right">' + _('Remove') + '</th>')
        output.append('</thead></tr>')
        return '\n'.join(output)

    def render_table_body(self, value):
        condominiums = [condominium for condominium in Condominium.objects.filter(pk__in=value).all()]
        output = []
        output.append('<tbody>')
        for condominium in condominiums:
            output.append(self.render_row(condominium))
        output.append('</tbody>')
        return '\n'.join(output)

    def render_row(self, condominium):
        return format_html('<tr value="{}"><td>{}</td><td class="td-actions text-right">'
                           '<a class="btn btn-danger btn-simple btn-xs"><i class="fa fa-times"></i></a></td>',
                           condominium.id, str(condominium))

    def value_from_datadict(self, data, files, name):
        return json.loads(data.get(name))


class CondominiumChoseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CondominiumChoseForm, self).__init__(*args, **kwargs)
        self.fields['condominiums'].required = False

    city = CityChoiceField(required=False, label=_('City'), widget=forms.Select(attrs={
        'title': _('Chose your city. Use search to find more.'),
        'class': 'selectpicker',
        'data-live-search': 'true'
    }))
    condominium = CondominiumChoiceField(required=False, label=_('Condominium'), widget=forms.Select(attrs={
        'title': _('Chose your condominium. Use search to find more.'),
        'class': 'selectpicker',
        'data-live-search': 'true',
        'disabled': True
    }))

    class Meta:
        model = get_user_model()
        fields = ['city', 'condominium', 'condominiums']
        widgets = {
            'condominiums': DisplayCondominiumsTable
        }


class CustomSearchForm(ModelSearchForm):
    q = forms.CharField(required=False, label=_('Search'),
                        widget=forms.TextInput(attrs={'placeholder': _('Enter text what you search.'),
                                                      'class': 'form-control input-lg'}))


class HouseAutoGenerationForm(forms.ModelForm):
    porch_count = forms.IntegerField(label=_('Porches count'), min_value=1)
    floor_count = forms.IntegerField(label=_('Floors count'), min_value=1)

    def __init__(self, *args, **kwargs):
        super(HouseAutoGenerationForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['porch_count'].initial = CondominiumPorch.objects.filter(house=self.instance).count()
            self.fields['floor_count'].initial = self.instance.max_floors


    class Meta:
        model = CondominiumHouse
        fields = ['address', 'area', 'residential_area', 'entrance_count', 'residential_count', 'elevators_count',
                  'porch_count', 'floor_count', 'description']
        exclude = ('name', 'condominium', 'object_registry', 'min_floors', 'max_floors',)
        widgets = {
            'address': forms.TextInput(attrs={
                'required': True,
            }),
            'area': forms.NumberInput(attrs={
                'min': 0.01,
                'step': 0.01,
                'required': True,
            }),
            'residential_area': forms.NumberInput(attrs={
                'min': 0,
                'step': 0.01,
                'required': True,
            }),
            'entrance_count': forms.NumberInput(attrs={
                'min': 0,
                'required': True,
            }),
            'residential_count': forms.NumberInput(attrs={
                'min': 0,
                'required': True,
            }),
            'elevators_count': forms.NumberInput(attrs={
                'min': 0,
                'required': True,
            }),
            'porch_count': forms.NumberInput(attrs={
                'required': True,
            }),
            'floor_count': forms.NumberInput(attrs={
                'required': True,
            })
        }

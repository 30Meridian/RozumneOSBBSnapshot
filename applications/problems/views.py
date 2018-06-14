from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied
from stronghold.decorators import public
from allauth.account.decorators import verified_email_required
from django.contrib import messages

from system.models import Condominium
from .models import Items, Statuses
from .forms import ItemsCreate

class ItemsForm(ModelForm):
    class Meta:
        model = Items
        fields = ['title', 'description', 'photo']

@public
def items_index(request, condominium_slug):
    return redirect('condominium:problems:items_list', condominium_slug=condominium_slug)

@public
def items_list(request, condominium_slug, template_name='problems/items_list.html'):
    condominium = getCondominium(condominium_slug)
    if request.user.is_authenticated() and request.session[
        'condominium_id'] in request.user.condominiums_list():
        items = Items.objects.all().filter(condominium_ref__slug=condominium_slug)
    else:
        items = Items.objects.all().filter(condominium_ref__slug=condominium_slug,
                                           public=1, condominium_ref__public_problems=1)
    data = {}
    data['object_list'] = items
    data['condominium'] = condominium
    return render(request, template_name, data)


@verified_email_required
def items_create(request, condominium_slug, template_name='problems/items_form.html'):
    condominium = getCondominium(condominium_slug)
    public_item = condominium.public_problems
    form = ItemsCreate(request.POST or None)
    if request.method == 'POST':
        form = ItemsCreate(request.POST or None, request.FILES)
        # fill a model from a POST
        if form.is_valid():
            instance = form.save(commit=False)
            instance.mainimg = form.cleaned_data['photo']
            instance.condominium_ref_id = condominium.id
            instance.user_ref_id = request.user.id
            instance.save()
            status = Statuses(
                status='pedding',
                item_ref_id=instance.id,
                owner_id=instance.user_ref_id
            )
            status.save()
            is_public = form.cleaned_data['public']
            if is_public:
                messages.warning(request, _('Warning! You have added public Item'))
            return redirect('condominium:problems:items_list', condominium_slug=condominium_slug)
        else:
            return render(request, template_name, {'form': form})
    else:
        form = ItemsCreate()
        return render(request, template_name, {'form': form, 'condominium': condominium})


# Отобразить новость
@public
def items_item(request, id, condominium_slug, template_name='problems/items_item.html'):
    condominium = getCondominium(condominium_slug)
    item = get_object_or_404(Items, id=id, condominium_ref__slug=condominium_slug)
    status_log = Statuses.objects.all().filter(item_ref_id=id)

    if not (request.user.is_authenticated() and
            request.session['condominium_id'] in request.user.condominiums_list()) and \
            not (item.public and item.condominium_ref.public_problems):
        raise PermissionDenied(_("Access denied"))

    return render(request, template_name, {'item': item, 'condominium': condominium, 'status_log': status_log,
                                           'last_status': status_log.reverse()[0]})


def getCondominium(condominium_slug):
    return Condominium.objects.filter(slug=condominium_slug).first()

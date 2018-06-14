from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView
from django.http import HttpResponse
from system.models import Condominium, CondominiumInfrastructure, CondominiumHouse, \
    CondominiumFloor, CondominiumResidentialPremise, CondominiumNonResidentialPremise,\
    CondominiumPorch


from .models import ManagementPages
from .forms import CondominiumUpdateForm

def index(request, condominium_slug):
    return info(request, condominium_slug)


def info(request, condominium_slug):
    condominium = Condominium.objects.filter(slug=condominium_slug).first()
    infrastructure = CondominiumInfrastructure.objects.filter(object_registry__condominium=condominium).all()
    return render(request, 'info.html', {'condominium': condominium, 'infrastructure': infrastructure})

def house_info(request, house_id, condominium_slug):
    house = get_object_or_404(CondominiumHouse,id=house_id)
    users = house.condominiumresidentialpremise_set.all().values_list('user', flat=True).distinct()
    return render(request, 'house_info.html', {'house': house, 'users_count': users.count})


class CondominiumUpdate(UpdateView):
    form_class = CondominiumUpdateForm
    template_name = 'edit.html'
    slug_url_kwarg = 'condominium_slug'

    def get_queryset(self):
        return Condominium.objects.all()

    def get_success_url(self):
        return reverse('condominium:summary', kwargs={'condominium_slug': self.object.slug})

    def render_to_response(self, context, **response_kwargs):
        if self.request.user in Condominium.objects.filter(slug=self.kwargs.get(self.slug_url_kwarg)).first().manager.all():
            return super(CondominiumUpdate, self).render_to_response(context, **response_kwargs)
        else:
            return HttpResponse(status=403)

edit = CondominiumUpdate.as_view()


def show_page(request, condominium_slug, path):
    page = ManagementPages.objects.filter(condominium__slug=condominium_slug).filter(slug=path).first()
    return render(request, 'page.html', {'page': page})


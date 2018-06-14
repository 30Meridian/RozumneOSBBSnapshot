from .models import Condominium
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, HttpResponseRedirect


def condominium_temp(request):
    condominium = None
    if 'condominium_id' in request.session and 'condominium_name' in request.session:
        condominium = request.session['condominium_id']

    if condominium:
        slug = Condominium.objects.get(pk=condominium).slug
        return {'condominium': True, 'menu': '', 'condominium_slug_header': slug}
    else:
        return {'condominium': False}


class CondominiumSessionMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        self.set_session_condominium(request, view_kwargs.get('condominium_slug'))

    @staticmethod
    def set_session_condominium(request, slug):
        if slug:
            try:
                condominium = Condominium.objects.get(slug=slug)
                request.session["condominium_id"] = condominium.id
                request.session["condominium_name"] = condominium.name
                request.session["condominium_slug"] = condominium.slug
            except ObjectDoesNotExist:
                return redirect('/')

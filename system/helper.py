from system.models import *
from django.utils.translation import ugettext_lazy as _

class Condominiums:
    '''Используется в списке городов по регионах'''
    def get_condominium(self, request, condominium_id):

        condominium_id = condominium_id
        condominium_name = ''
        set_cookie = None

        if(condominium_id == None) and (request.session.has_key('condominium')):
            condominium = request.session['condominium']
            if(condominium):
                condominium_id = condominium
                condominium_name = self._get_condominium_name(condominium_id)
            else:
                return _('Condominium did not find in urls and cookies')
        elif(condominium_id) and not (request.session.has_key('condominium')):
            condominium_name = self._get_condominium_name(condominium_id)
            set_cookie = True
        elif not(condominium_id) and not (request.session.has_key('condominium')):
            if(request.user.is_authenticated()):
                condominium = User.objects.get(id=request.user.id).condominiums.all()[0]
                condominium_id = condominium.id
                set_cookie = True
                condominium_name = self._get_condominium_name(condominium_id)
        else:
            return None

        return {'condominium_id': condominium_id, 'condominium_name': condominium_name, 'set_cookie': set_cookie}

    def _get_condominium_name(condominium_id):
        if(condominium_id):
            condominium_name = Condominiums.objects.get(id=condominium_id).name
            return condominium_name
        else:
            return 'Вкажіть ID міста'

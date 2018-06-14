from django import template
from django.utils.translation import ugettext_lazy as _

from ..models import Modules, CondominiumModules, CondominiumResidentialPremise, CondominiumHouse

register = template.Library()


@register.assignment_tag
def menu(condominium_slug):
    try:
        condominium_modules = CondominiumModules.objects.filter(condominium__slug=condominium_slug, use=True)\
            .order_by('weight').select_related('module')

        result = []
        module_id = 0
        for modules in condominium_modules.all():
            module = modules.module
            module_id += 1
            module_response = {
                'id': 'Menu' + str(module_id),
                'slug': module.slug,
                'text': str(_(module.title)),
                'icon': module.icon,
                'child': None
            }

            child_modules = Modules.all_objects.filter(parent=module).all()
            if len(child_modules):
                children = []
                for child_module in child_modules:
                    children.append({
                        'slug': child_module.slug,
                        'text': str(_(child_module.title))
                    })
                module_response['child'] = children
            result.append(module_response)

        return result
    except CondominiumModules.DoesNotExist:
        return []


@register.assignment_tag
def concat(str_a, *args):
    res = str_a
    for str_b in args:
        res += str_b
    return res


@register.filter(name='add_css')
def add_css(value, arg):
    return value.as_widget(attrs={'class': arg if 'class' not in value.field.widget.attrs else
    value.field.widget.attrs['class'] + ' ' + arg })


@register.filter(name='active')
def active(url, request):
    full_path = request.get_full_path()
    if full_path.startswith(url):
        return True
    else:
        return False


@register.assignment_tag
def check_premise(user, session):
    flag = True
    if 'condominium_id' in session:
        query = CondominiumResidentialPremise.objects.filter(user=user, house__condominium=session['condominium_id'])
        house_query = CondominiumHouse.objects.filter(condominium=session['condominium_id'])
        if query.count() > 0 or house_query.count() == 0:
            flag = False
    else:
        flag = False
    return flag

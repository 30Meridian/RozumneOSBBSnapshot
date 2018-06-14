from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from modules.machina.core.db.models import get_model

from .models import ObjectTypes, Condominium, CondominiumPorch, CondominiumFloor


class DecoratedURLPattern(RegexURLPattern):
    def resolve(self, *args, **kwargs):
        result = super(DecoratedURLPattern, self).resolve(*args, **kwargs)
        if result:
            result.func = self._decorate_with(result.func)
        return result


class DecoratedRegexURLResolver(RegexURLResolver):
    def resolve(self, *args, **kwargs):
        result = super(DecoratedRegexURLResolver, self).resolve(*args, **kwargs)
        if result:
            result.func = self._decorate_with(result.func)
        return result


def decorated_includes(func, includes, *args, **kwargs):
    urlconf_module, app_name, namespace = includes

    for item in urlconf_module:
        if isinstance(item, RegexURLPattern):
            item.__class__ = DecoratedURLPattern
            item._decorate_with = func

        elif isinstance(item, RegexURLResolver):
            item.__class__ = DecoratedRegexURLResolver
            item._decorate_with = func

    return urlconf_module, app_name, namespace


def forum_condominium_permission(func):
    def new_function(*args, **kwargs):
        forum = get_model('forum', 'Forum')
        if 'forum_slug' in kwargs:
            curr = forum.objects.filter(slug=kwargs['forum_slug']).first()
            if not curr.condominium in args[0].user.condominiums.all():
                return HttpResponse(status=403)
        return func(*args, **kwargs)

    return new_function


def manage_condominium_permission(func):
    def new_function(request, *args, **kwargs):
        manager_in_condominiums = Condominium.objects.filter(manager=request.user)
        if manager_in_condominiums:

            flag = True
            if 'condominium_slug' in request.session:
                if len(manager_in_condominiums.filter(slug=request.session['condominium_slug'])) > 0:
                    flag = False

            if flag:
                condominium = manager_in_condominiums.first()
                request.session['condominium_id'] = condominium.id
                request.session['condominium_name'] = condominium.name
                request.session['condominium_slug'] = condominium.slug

            return func(request, *args, **kwargs)
        elif request.user.is_editor():
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied("Доступ заборонено")

    return new_function


def generate_house_from_form(request, obj, form):
    if form.is_valid():
        porch_count = form.cleaned_data['porch_count']
        floor_count = form.cleaned_data['floor_count']
        floor_type = ObjectTypes.objects.filter(title='Common', category='Floor').first()

        prev_porch_count = CondominiumPorch.objects.filter(house=obj).count()
        prev_floor_count = obj.max_floors

        obj.condominium = Condominium.objects.get(slug=request.session['condominium_slug'])
        obj.min_floors = floor_count
        obj.max_floors = floor_count

        obj.save()

        if (prev_porch_count is None or prev_porch_count == 0) and \
                (prev_floor_count is None or prev_floor_count == 0):
            for i in range(1, porch_count + 1):
                porch = CondominiumPorch.objects.create(house=obj, number=i, floors_count=floor_count)
                for j in range(1, floor_count + 1):
                    CondominiumFloor.objects.create(porch=porch, number=j, type=floor_type)
        else:
            if prev_porch_count > porch_count:
                porches = CondominiumPorch.objects.filter(house=obj).order_by('-number')
                porches = porches[:prev_porch_count - porch_count]
                for porch in porches:
                    porch.delete()
            elif prev_porch_count < porch_count:
                for i in range(prev_porch_count + 1, porch_count + 1):
                    porch = CondominiumPorch.objects.create(house=obj, number=i, floors_count=floor_count)
                    for j in range(1, prev_floor_count + 1):
                        CondominiumFloor.objects.create(porch=porch, number=j, type=floor_type)

            if prev_floor_count > floor_count:
                porches = CondominiumPorch.objects.filter(house=obj)
                for porch in porches:
                    floors = CondominiumFloor.objects.filter(porch=porch).order_by('-number')
                    floors = floors[:prev_floor_count - floor_count]
                    for floor in floors:
                        floor.delete()
            elif prev_floor_count < floor_count:
                porches = CondominiumPorch.objects.filter(house=obj)
                for porch in porches:
                    for j in range(prev_floor_count + 1, floor_count + 1):
                        CondominiumFloor.objects.create(porch=porch, number=j, type=floor_type)

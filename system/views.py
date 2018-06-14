import os
import urllib.parse as urllib_parse
import system

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from datetime import datetime
from django.contrib import messages
from stronghold.decorators import public
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from filemanager import FileManager

from django.views.generic import TemplateView
from problems.models import Items, Statuses

from .forms import ResidentialPremiseAddForm, NonResidentialPremiseAddForm, CondominiumCreateForm, \
    CondominiumChoseForm, UserForm, HouseAutoGenerationForm
from .models import User, Condominium, ObjectRegistry, CondominiumConnectedUtility, City, CondominiumHouse, \
    CondominiumResidentialPremise, CondominiumNonResidentialPremise
from .settings import MEDIA_ROOT
from .utils import generate_house_from_form

from requests import request as send_request
from json import loads as parse_json
from random import random

def index(request):
    """
    Resolving call of base url
    :param request: Django http request
    :return: Info page for not authenticated users and specific redirect for authenticated
    """
    if request.user.is_authenticated():
        if len(request.user.condominiums.all()) > 0:
            response = HttpResponseRedirect(reverse('condominium:summary',
                                                    args=[request.user.condominiums.all()[0].slug]))
            if 'condominium_slug' in request.session:
                if Condominium.objects.get(slug=request.session['condominium_slug']) in request.user.condominiums.all():
                    response = HttpResponseRedirect(reverse('condominium:summary',
                                                            args=[request.session['condominium_slug']]))
        else:
            response = HttpResponseRedirect(reverse('condominium_update', args=[request.user.id]))
    else:
        response = HttpResponseRedirect(reverse('blog:index'))

    return response


def redirect_to_summary(request, condominium_slug):
    """
    Write session for particular condominium
    :param request: Django http request
    :param condominium_slug: Slug of chosen condominium
    :return: Redirect to condominium home page
    """
    query = Condominium.objects.filter(slug=condominium_slug)
    if query.count() == 0:
        return HttpResponseRedirect(reverse('index'))

    condominium = query.first()
    if condominium in request.user.condominiums.all():
        request.session['condominium_id'] = condominium.id
        request.session['condominium_name'] = condominium.name
        request.session['condominium_slug'] = condominium.slug
    return HttpResponseRedirect(reverse('condominium:home', args=[condominium_slug]))


def errorPage(request, condominium_slug, broken_link):
    return render(request, 'error.html',
                  {'desc': _("This reference on module is wrong or module is not exists.")})


@public
def index_condominium(request, condominium_slug):
    """
    Condominium home page management
    :param request: Django http request
    :param condominium_slug: Slug of chosen condominium
    :return: Rendered home template for particular stage of condominium life
    """
    query = Condominium.objects.filter(slug=condominium_slug)
    if query.count() == 0:
        return HttpResponseRedirect(reverse('index'))

    condominium = query.first()
    if request.method == 'GET':
        issues = None
        ideas = None
        news = None
        polls = None
        allowed = None
        topics = None

        # if 1 in modules:  # Дефекты ЖКХ
        from defects.models import Issues
        issues = [i for i in Issues.objects.filter(parent_task_ref=None, condominium_ref=condominium).
            order_by('-id') if i.last_issue().status != 0 and i.last_issue().status != 3]

        from ideas.models import Ideas
        from news.models import News
        from polls.models import Poll

        if request.user.is_authenticated() and request.session['condominium_id'] in request.user.condominiums_list():
            ideas = Ideas.objects.filter(condominium=condominium, status=2).order_by('-id')[:3]
            news = News.objects.filter(condominium=condominium, publish=1, datetime_publish__lte=datetime.now).order_by(
                '-datetime_publish')[:3]
            polls = Poll.objects.filter(active=1, archive=0, condominium=condominium).order_by('id')[:3]
            items = Items.objects.filter(condominium_ref=condominium).order_by('-create')[:3]
        else:
            ideas = Ideas.objects.filter(condominium=condominium, status=2,
                                         public=1, condominium__public_ideas=1).order_by('-id')[:3]
            news = News.objects.filter(condominium=condominium, publish=1,
                                       datetime_publish__lte=datetime.now, public=1,
                                       condominium__public_news=1).order_by('-datetime_publish')[:3]
            polls = Poll.objects.filter(active=1, archive=0, condominium=condominium,
                                        public=1, condominium__public_polls=1).order_by('id')[:3]
            items = Items.objects.filter(condominium_ref=condominium, public=1, condominium_ref__public_problems=1).order_by('-create')[:3]


        if request.user.is_authenticated() and request.session['condominium_id'] in request.user.condominiums_list():
            from machina.apps.forum_conversation.models import Topic
            topics = Topic.objects.filter(forum__condominium=condominium).order_by('-created')[:3]

        if ideas or news or polls or items or topics:
            return render(request, 'summarypage.html',
                          {'condominium': condominium,
                           'issues': issues,
                           'ideas': ideas,
                           'news': news,
                           'polls': polls,
                           'items': items,
                           'topics': topics,
                           })
        else:
            if request.user.is_authenticated():
                has_house = False if CondominiumHouse.objects.filter(condominium=condominium).count() == 0 else True
                form = HouseAutoGenerationForm()
                form.base_fields['address'].initial = condominium.legal_address

                if condominium_slug in request.user.is_manager():
                    return render(request, 'summarypage_for_new.html',
                                  {'condominium': condominium, 'has_house': has_house, 'form': form})
                else:
                    return render(request, 'summarypage_for_new_user.html')
            else:
                return render(request, 'summarypage.html', {'condominium': condominium,})
    else:
        form = HouseAutoGenerationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            generate_house_from_form(request, instance, form)

            response = HttpResponseRedirect(reverse('condominium:summary', args=[condominium_slug]))
        else:
            response = render(request, 'summarypage_for_new.html',
                              {'condominium': condominium, 'has_house': False, 'form': form})
        return response

# страница регионов
def ourmasters(request, condominium_slug):
    return render(request, 'ourmasters.html')


# страница регионов
def tariffs(request, condominium_slug):
    return render(request, 'tariffs.html')


# страница регионов
def documents(request, condominium_slug):
    return render(request, 'documents.html')


def about(request):
    return render(request, 'about.html')


def help_page(request):
    return render(request, 'help.html')


def contacts(request):
    return render(request, "contacts.html")

def instructions(request):
    return render(request, "instructions.html")

def profile(request, user_id):
    """
    Показываем профиль пользователя
    :param request: Standard view input
    :param user_id: User identification
    :return: Profile page if all correct or redirect on login page.
    """
    if request.user.is_authenticated() and request.user.is_active:
        user = get_object_or_404(User, pk=user_id)
        condominiums_list = user.condominiums.all()
        # list of users who can get your personal info like phone number (friends of this user)
        allowed = []
        return render(request, 'profile.html', {'allowed': allowed,
                                                'user': user,
                                                'condominiums': condominiums_list,
                                                'residential_premise': user.residential_premise,
                                                'non_residential_premise': user.non_residential_premise,
                                                })
    else:
        return redirect('/account/login')


class UserUpdate(UpdateView):
    form_class = UserForm
    model = User
    template_name = 'edit.html'
    pk_url_kwarg = 'user_id'

    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.kwargs.get(self.pk_url_kwarg)})

    def render_to_response(self, context, **response_kwargs):
        if str(self.request.user.id) == str(self.kwargs.get(self.pk_url_kwarg)):
            return super(UserUpdate, self).render_to_response(context, **response_kwargs)
        else:
            return HttpResponse(status=403)


profile_edit = UserUpdate.as_view()


class AddResidentialPremise(CreateView):
    form_class = ResidentialPremiseAddForm
    template_name = 'edit.html'

    def get_form_kwargs(self):
        kwargs = super(AddResidentialPremise, self).get_form_kwargs()
        kwargs['condominiums'] = self.request.user.condominiums.all()
        return kwargs

    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.request.user.id})

    def render_to_response(self, context, **response_kwargs):
        if str(self.request.user.id) == str(self.kwargs.get('user_id')):
            return super(AddResidentialPremise, self).render_to_response(context, **response_kwargs)
        else:
            return HttpResponse(status=403)

    def form_valid(self, form):
        response = super(AddResidentialPremise, self).form_valid(form)

        registry = ObjectRegistry(condominium_id=self.request.session['condominium_id'], type=form.cleaned_data['type'],
                                  user_created=self.request.user, user_changed=self.request.user,
                                  title=_(str(self.object)[:64]))
        registry.save()

        self.object.user = self.request.user
        self.object.object_registry = registry
        self.object.save()

        return response


residential_premise_create = AddResidentialPremise.as_view()


class DeleteResidentialPremise(DeleteView):
    model = CondominiumResidentialPremise
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.id])


residential_premise_delete = DeleteResidentialPremise.as_view()


class AddNonResidentialPremise(CreateView):
    form_class = NonResidentialPremiseAddForm
    template_name = 'edit.html'

    def get_form_kwargs(self):
        kwargs = super(AddNonResidentialPremise, self).get_form_kwargs()
        kwargs['condominiums'] = self.request.user.condominiums.all()
        return kwargs

    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.request.user.id})

    def render_to_response(self, context, **response_kwargs):
        if str(self.request.user.id) == str(self.kwargs.get('user_id')):
            return super(AddNonResidentialPremise, self).render_to_response(context, **response_kwargs)
        else:
            return HttpResponse(status=403)

    def form_valid(self, form):
        response = super(AddNonResidentialPremise, self).form_valid(form)

        registry = ObjectRegistry(condominium_id=self.request.session['condominium_id'], type=form.cleaned_data['type'],
                                  user_created=self.request.user, user_changed=self.request.user,
                                  title=_(str(self.object)[:64]))
        registry.save()

        self.object.user = self.request.user
        self.object.object_registry = registry
        self.object.save()

        return response


non_residential_premise_create = AddNonResidentialPremise.as_view()


class DeleteNonResidentialPremise(DeleteView):
    model = CondominiumNonResidentialPremise
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.id])


non_residential_premise_delete = DeleteNonResidentialPremise.as_view()


def karma(request, user_id):
    if request.user.is_authenticated() and request.user.is_active:
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        points = 1
        return render(request, 'karma_list.html', {'points': points})
    else:
        return redirect('/account/login')


def userban(request, user_id, status):
    if (request.user.is_authenticated() and request.user.is_active):
        user = get_object_or_404(User, pk=user_id)
        moder = request.user.isAllowedToModerate(request.session['condominium'], 'Profile')
        allowed = (user.condominiums.all()[0] in [t for t in request.user.condominiums.all()] and moder)
        if (allowed):
            user.is_active = int(status)
            user.save()
            return redirect('/profile/' + user_id)
        else:
            raise PermissionDenied(_('Access not allowed'))
    else:
        raise PermissionDenied(_('Access not allowed'))


# показываем пользователю после регистрации
def confirmyouremail(request):
    return render(request, 'please_confirm_your_email.html')


# контакты модераторов
def moderators(request, condominium_slug):
    if ('condominium' in request.session):
        moders = Condominium.objects.get(pk=request.session['condominium']).additions.filter(type='moderators')[0].body
        return render(request, 'moderators_info_page.html', {'moders': moders})
    else:
        return redirect('regions')


def people(request, condominium_slug):
    """
    Generate context and call render a page of neighborhoods.
    :param request: Django request
    :param condominium_slug: Condominium unique identification and adress
    :return: Page of neighborhoods.
    """
    if request.user.is_authenticated() and request.user.is_active:
        condominium = Condominium.objects.get(slug=condominium_slug)
        users = condominium.user_set.all()
        # flats = CondominiumResidentialPremise.objects.filter(type=_('Flat'))
        return render(request, 'people.html', {'users': users})
    else:
        raise PermissionDenied


# Рейтинг пользователей
def rating(request, condominium_slug):
    if 'condominium' in request.session and 'condominium_name' in request.session:
        from django.db.models import Sum
        list_ = []
        for user in get_object_or_404(Condominium, pk=request.session['condominium']).user_set.all().annotate(
                points_sum=Sum('karma__points')).order_by('-points_sum'):
            if not user.isAllowedToModerate(request.session['condominium']):
                u = user
                list_.append(u)

        if (request.POST):
            list_ = list_[:3]
            return render_to_response('_rating-ajax.html', {'list': list_})
        else:
            return render(request, 'user_rating.html', {'list': list_})
    else:
        return redirect('regions')


# выловить динамический url и показать документ
def getDocums(request, url_param, condominium_slug):
    if ('condominium' in request.session):
        try:
            doc = get_object_or_404(Condominium, pk=request.session['condominium']).additions.get(type=url_param)
        except:
            raise ObjectDoesNotExist(_('This object is not exist.'))
        ###############

        return render(request, 'docs.html', {'doc': doc})
    else:
        return redirect('regions')
    return render(request, 'docs.html', {'doc': doc})


def handler404(request):
    response = render_to_response('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {}, context_instance=RequestContext(request))
    response.status_code = 500
    return response


@csrf_exempt
def condominium_active_search(request):
    result = []
    for t in request.user.condominiums.all():
        condominium = {}
        condominium['name'] = t.name
        condominium['slug'] = t.slug
        result.append(condominium)
    return JsonResponse(result, safe=False)


def condominiumRedirect(request, condominiumredirect):
    return redirect('/%s' % condominiumredirect)


@csrf_exempt
def condominium_active_search_for_manage(request):
    result = []
    for t in Condominium.objects.filter(manager=request.user):
        condominium = {}
        condominium['name'] = t.name
        condominium['slug'] = t.slug
        result.append(condominium)
    return JsonResponse(result, safe=False)


def redirect_to_manage(request, condominium_slug):
    if 'condominium_id' in request.session and 'condominium_name' in request.session and 'condominium_slug' in request.session:
        condominium = Condominium.objects.filter(slug=condominium_slug).first()
        request.session['condominium_id'] = condominium.id
        request.session['condominium_name'] = condominium.name
        request.session['condominium_slug'] = condominium.slug
        return redirect('/manage')


class CreateUtility(CreateView):
    model = CondominiumConnectedUtility
    fields = ['service', 'object_registry', 'start_value']
    template_name = 'edit.html'

    def get_success_url(self):
        return '/profile/{}'.format(self.request.user.id)


#
manage_utilities = CreateUtility.as_view()


class DashboardMainView(TemplateView):
    template_name = 'admin/own_index.html'

    def get(self, request, *args, **kwargs):
        condominium = Condominium.objects.filter(id=request.session['condominium_id']).first()
        users = condominium.user_set.filter(condominiums=condominium).order_by('-last_login')
        ideas = condominium.ideas_set.filter(condominium=condominium).order_by('-create_date')
        news = condominium.news_set.filter(condominium=condominium).order_by('-datetime')
        problems_qs = Items.objects.filter(condominium_ref=request.session['condominium_id']).order_by('-last_update')

        managers_condominium = Condominium.objects.filter(manager=request.user)

        ideas_for_consideration = ideas.filter(status=1)
        problems_for_consideration = []
        for problem in problems_qs:
            if problem.problems_items.count() > 0:
                if str(problem.problems_items.all().order_by('-create')[0]) == _('pedding'):
                    problems_for_consideration.append(problem)
        try:
            page_problem = request.GET.get('page_pr', 1)
            page_idea = request.GET.get('page_idea', 1)
        except PageNotAnInteger:
            page_problem = 1
            page_idea = 1

        p_problems = Paginator(problems_for_consideration, 5, request=request)
        problems = p_problems.page(page_problem)

        p_ideas = Paginator(ideas_for_consideration, 5, request=request)
        ideas_list = p_ideas.page(page_idea)

        context = ({
            'users': users[:3],
            'ideas': ideas[:3],
            'news': news[:3],
            'managers_condominium': managers_condominium,
            'users_count': users.count,
            'ideas_count': ideas.count,
            'news_count': news.count,
            'ideas_list': ideas_list,
            'problems': problems,
        })
        return self.render_to_response(context)


class AdminHelpView(TemplateView):
    template_name = 'admin/help.html'


class UpdateCondominiumsView(UpdateView):
    template_name = 'condominiums_update.html'
    form_class = CondominiumChoseForm
    form_second_class = CondominiumCreateForm
    pk_url_kwarg = 'user_id'

    def get_success_url(self):
        return '/'  # self.request.get_full_path()

    def get_queryset(self):
        return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super(UpdateCondominiumsView, self).get_context_data(**kwargs)
        if 'create_form' in kwargs:
            context['create_form'] = kwargs['create_form']
        else:
            context['create_form'] = self.form_second_class(prefix='create')
        context['api_key'] = system.settings.GOOGLE_API_KEY
        return context

    def post(self, request, *args, **kwargs):
        response = super(UpdateCondominiumsView, self).post(request, *args, **kwargs)

        form_create = self.form_second_class(request.POST, request.FILES, prefix='create')
        if form_create.has_changed():
            if form_create.is_valid():
                resp = form_create.save()
                resp.manager.add(request.user)

                request.user.is_staff = True
                request.user.save()
                request.user.groups.add(Group.objects.get(name='manager'))
                request.user.groups.remove(Group.objects.get(name='user'))
                request.user.condominiums.add(resp)

                response = HttpResponseRedirect(reverse('condominium:summary', args=(resp.slug,)))

                # if
                ideas = form_create.cleaned_data['public_ideas']
                news = form_create.cleaned_data['public_news']
                problems = form_create.cleaned_data['public_problems']
                polls = form_create.cleaned_data['public_polls']
                if ideas or news or problems or polls:
                    messages.warning(request, _('Warning. Next modules will be public: {ideas} {news} {problems} {polls} You can change it in admin page.').format(
                            ideas=_('Ideas')+';' if ideas else '',
                            news=_('News')+';' if news else '',
                            problems=_('Problems')+';' if problems else '',
                            polls=_('Polls')+';' if polls else '',
                            ))

                response = HttpResponseRedirect(reverse('condominium:summary', args=[resp.slug]))
            else:
                response = self.render_to_response(self.get_context_data(form=self.form_class(request.POST),
                                                                         create_form=form_create
                                                                         ))

        return response


update_condominiums = UpdateCondominiumsView.as_view()


def document_view(request, condominium_slug, path):
    fm = FileManager(os.path.join(os.path.join(MEDIA_ROOT, 'documents'), str(condominium_slug)),
                     is_admin_view=True if condominium_slug in request.user.is_manager() else False)
    return fm.render(request, path)


@csrf_exempt
def filter_cities(request):
    filter_ = None
    if request.POST:
        # parse shielded symbols in filter
        filter_ = urllib_parse.unquote(request.POST['filter'])

    # filter record in town model exclude city areas
    if filter_:
        town_qs = City.objects.filter(is_residential=True).filter(specialized_name__startswith=filter_.upper()) \
            .exclude(prefix='р-н').all()
    else:
        town_qs = City.objects.filter(is_residential=True).exclude(prefix='р-н').all()

    result = []
    for record in town_qs[:50]:
        result.append({
            'id': record.id,
            'value': str(record)
        })
    return JsonResponse(result, safe=False)


@csrf_exempt
def filter_condominiums(request):
    filter_ = None
    if request.POST:
        # parse shielded symbols in filter
        filter_ = urllib_parse.unquote(request.POST['filter'])

    # filter record in condominium model
    if filter_:
        condominium_qs = Condominium.objects.filter(city=int(filter_))
    else:
        condominium_qs = Condominium.objects.all()

    result = []
    for record in condominium_qs:
        result.append({
            'id': record.id,
            'value': str(record)
        })
    return JsonResponse(result, safe=False)


def load_condominium_coordinates(request):
    if request.user.is_superuser:
        condominiums = Condominium.objects.all()
        for condominium in condominiums:

            address = get_address(condominium.city.specialized_name, condominium.legal_address)
            data = send_geocode_request(address)

            if data['status'] == 'OK':
                location = data['results'][0]['geometry']['location']
                save_lat_lon(condominium, location)
                print('done')
            else:
                address = get_address(legal_address=condominium.legal_address)
                data = send_geocode_request(address)

                if data['status'] == 'OK':
                    location = data['results'][0]['geometry']['location']
                    save_lat_lon(condominium, location)
                    print('done')
                else:
                    address = get_address(city=condominium.city.specialized_name)
                    data = send_geocode_request(address)
                    if data['status'] == 'OK':
                        location = data['results'][0]['geometry']['location']
                        if random() > 0.5:
                            location['lat'] += random() / 1000
                        else:
                            location['lat'] -= random() / 1000
                        if random() > 0.5:
                            location['lng'] += random() / 1000
                        else:
                            location['lng'] -= random() / 1000

                        save_lat_lon(condominium, location)
                        print('done with city')
                    else:
                        print('address not correct')

        return redirect('/')
    else:
        return redirect('/')


def save_lat_lon(condominium, location):
    latitude = location['lat']
    longitude = location['lng']

    condominium.latitude = latitude
    condominium.longitude = longitude
    condominium.save()


def get_address(city='', legal_address=''):
    address = None

    if legal_address and city:
        address = city + ',' + legal_address
    elif not city:
        address = legal_address
    elif not legal_address:
        address = city

    return address


def send_geocode_request(address):
    url = 'http://maps.googleapis.com/maps/api/geocode/json?address={}'
    current_url = url.format('Україна'+address.lower())
    response = send_request(method='get', url=current_url)
    data = parse_json(response.text)
    return data

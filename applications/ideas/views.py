from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import *
from .models import IdeasStatuses,Ideas, IdeasVoices
from defects.models import Condominium, User
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from .helper import Activity, ActivityMail
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
import datetime
import time
from ipware.ip import get_ip
from system.settings import CRON_SECRET, KARMA
from allauth.account.decorators import verified_email_required
from django.utils.translation import ugettext_lazy as _
from stronghold.decorators import public

# если админ или модер - показываем на главной петиции на модерации
@public
def index(request, condominium_slug):
    return redirect('../ideas/status/2')

#добавляем петицию (показываем форму)
@verified_email_required
def add(request, condominium_slug):
    public_idea = Condominium.objects.get(id=request.session['condominium_id']).public_ideas
    if(request.user.is_authenticated() and request.user.is_active):
        if request.method == 'POST':
            form = IdeaAdd(request.POST, request.FILES, )
            #fill a model from a POST
            if form.is_valid():
                user = request.user
                instance = form.save(commit=False)
                instance.owner_user = user
                instance.condominium = Condominium.objects.get(id=request.session['condominium_id'])
                instance.status = IdeasStatuses.objects.get(pk=1)
                instance.image = form.cleaned_data['image']
                instance.save()
                Activity().add_robot(request, instance.id, _('Idea created'))
                ActivityMail.sendToModers(request,_('New idea moved to moderation'), 'idea_new.email', instance.condominium.id, {'idea_id':instance.id, 'title': instance.title,'condominium_slug':condominium_slug})
                ActivityMail.sendToModers(request,_('Your idea moved to moderation'), 'idea_change_status.email', instance.condominium.id, {'idea_id':instance.id, 'title': instance.title, 'status':'На модерації','condominium_slug':condominium_slug}, [instance.owner_user.email] )
                is_public = form.cleaned_data['public']
                if is_public:
                    messages.warning(request, _('Warning! You have added public Idea'))
                return render(request,'thank_you.html')
            else:

                return render(request, 'add_idea.html', {'form': form})
        else:
            form = IdeaAdd()
            # form = IdeaAdd(initial={'public': public_idea})
            # form.fields['public'].initial = True
            return render(request, 'add_idea.html', {'form': form})
    else:
        redirect('accounts/signup')


# #проверяем кроном просроченые петиции и переносим в архивные
def checktimeout(request, secret, condominium_slug):
    if(secret == CRON_SECRET):
       ideas = Ideas.objects.filter(status=2)
       count = 0
       status = IdeasStatuses.objects.get(pk=5)
       for idea in ideas:
           need_votes =  idea.condominium.votes
           ideas_days = idea.condominium.ideas_days
           date_start = idea.when_approve
           days_end = date_start + datetime.timedelta(days=ideas_days)
           day_now = datetime.datetime.now()
           days_left = days_end - day_now

           if(days_left.days < 0):
               idea.status= status # делаем архивной если у петиции кончилось время сбора подписей и она не набрала нужного количества голосов
               idea.save()
               Activity().add(request, idea.id, _('Automatic status change to "Archive"'))
               ActivityMail.sendToModers(request, _('The idea has not collected the necessary number votes and moved to the archive.'), 'idea_change_status.email', idea.condominium.id, {'idea_id':idea.id, 'title': idea.title, 'status':'Архівна','condominium_slug':condominium_slug})
               ActivityMail.sendToModers(request, _('Your idea has not collected the necessary number votes and moved to the archive.'), 'idea_change_status.email', idea.condominium.id, {'idea_id':idea.id, 'title': idea.title, 'status':'Архівна','condominium_slug':condominium_slug}, [idea.owner_user.email])
               count +=1

       if(count):
           return HttpResponse('Done! Find: '+str(count)+' idea(-s)')
       else:
           return HttpResponse(_("Not found any ideas that mutch enddate!"))
    else:
        raise PermissionDenied(_('Access denied.'))

#Отображаем петицию
@public
def idea(request, idea_id, condominium_slug):
       idea = get_object_or_404(Ideas,id=idea_id)
       condominium = Condominium.objects.get(id=idea.condominium.id)
       need_votes =  condominium.votes
       ideas_days = condominium.ideas_days
       idea_number = condominium.ideas_number_templ % (idea_id)
       allowed = False
       activities = None
       if not 'condominium_id' in request.session:
           request.session['condominium_id'] = idea.condominium.id
           request.session['condominium_name'] = idea.condominium.name
           request.session['condominium_slug'] = idea.condominium.slug
           allowed = False

       if(idea.status.id == 1 and not allowed):
           raise PermissionDenied(_("You can't view ideas what are on moderation"))

       if(allowed):
          activities = idea.ideasactivity_set.all().order_by("-id")

       if not (request.user.is_authenticated() and
           request.session['condominium_id'] in request.user.condominiums_list()) and not (idea.public and condominium.public_ideas):
           raise PermissionDenied(_("Access denied"))

       try:
            page = request.GET.get('page', 1)
       except PageNotAnInteger:
            vpage = 1

       p = Paginator(IdeasVoices.objects.filter(idea=idea_id).exclude(block=1).all(),9, request=request)
       votes = p.page(page)
       votes_count =  IdeasVoices.objects.filter(idea=idea_id).exclude(block=1).all().count()
       fullname =  get_object_or_404(User,id = idea.owner_user.id).get_full_name()
       end_date = False

       if(idea.status.id == 5):
           date_start = idea.when_approve
           end_date = date_start + datetime.timedelta(days=ideas_days)

       if(idea.status.id == 2):
           date_start = idea.when_approve
           days_end = date_start + datetime.timedelta(days=ideas_days)
           day_now = datetime.datetime.now()
           days_left = days_end - day_now
           days_passed = day_now - date_start
           return render(request, 'idea.html',{
               'idea': idea,
               'days_left': days_left.days,
               'ideas_days':ideas_days,
               'days_passed': days_passed.days,
               'needvotes':need_votes,
               'idea_number': idea_number,
               'fullname': fullname,
               'votes': votes,
               'votes_count': votes_count,
               'allowed': allowed,
               'getusersign': _getusersign(request, idea_id),
               'activities': activities,
               'end_date':end_date,
           })
       else:
           return render(request, 'idea.html',{'idea': idea, 'ideas_days':ideas_days, 'needvotes':need_votes,'fullname': fullname,'idea_number': idea_number,'allowed': allowed, 'votes': votes, 'getusersign': _getusersign(request,idea_id),'activities':activities, 'end_date':end_date })


# Показываем список петиций
@public
def list(request, status, condominium_slug):

    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    if 'condominium_id' in request.session:
        if request.user.is_authenticated() and request.session['condominium_id'] in request.user.condominiums_list():
            p = Paginator(Ideas.objects.filter(condominium = request.session['condominium_id'], status = status).order_by("-id"), 25, request=request)
        else:
            p = Paginator(
                Ideas.objects.filter(condominium=request.session['condominium_id'], status=status, public=1, condominium__public_ideas=1).order_by("-id"), 25,
                request=request)
        ideas = p.page(page)
        condominium = Condominium.objects.get(slug=request.session['condominium_slug'])
        need_votes = condominium.votes
        if status == '2':
            return render(request, 'ideas_list_2.html',{'ideas': ideas, 'need_votes': need_votes})
        elif status == '3':
            return render(request, 'ideas_list_3.html',{'ideas': ideas})
        elif status == '4':
            return render(request, 'ideas_list_4.html',{'ideas': ideas})
        elif status == '5':
            return render(request, 'ideas_list_5.html',{'ideas': ideas, 'need_votes': need_votes})
        elif status == '6':
            return render(request, 'ideas_list_6.html',{'ideas': ideas})
    else:
        return redirect(reverse('regions'))


#Правила петиций
def rules(request, condominium_slug):
    return render(request, 'rules.html')


#Помощь
def help(request, condominium_slug):
    return render(request, 'help_idea.html')

#отдать cвой голос
@verified_email_required
def vote(request, idea_id, condominium_slug):
    if(request.user.is_authenticated() and request.user.is_active):
        idea = get_object_or_404(Ideas, id=idea_id)
        if idea.condominium in request.user.condominiums.all():
            vote = IdeasVoices()
            vote.idea_id = idea_id
            vote.user = request.user
            vote.ip = get_ip(request)
            vote.save()
            #Karma.add(request.user,KARMA['PETITION_VOTE'],"Голосування за ідею", "Ідеї")
            votes_count =  IdeasVoices.objects.filter(idea=idea_id).exclude(block=1).all().count()
            if (votes_count ==  idea.condominium.votes):
                status = IdeasStatuses.objects.get(pk=8)
                idea.status = status
                idea.save()

                Activity().add(request, idea_id, _('Automatic status change to "Verification votes"'))
                ActivityMail.sendToModers(request, _('The idea has the necessary number of votes. Check signatures.'), 'idea_change_status.email', idea.condominium.id, {'idea_id':idea.id, 'title': idea.title, 'status':'На перевірці голосів','condominium_slug':condominium_slug})
                ActivityMail.sendToModers(request, _('Your idea has the necessary number of votes and has moved to signatures check'), 'idea_change_status.email', idea.condominium.id, {'idea_id':idea.id, 'title': idea.title, 'status':'На перевірці голосів','condominium_slug':condominium_slug}, [idea.owner_user.email])
            return redirect('../../ideas/%s' % idea_id)
        else:
            raise PermissionDenied(_('Access denied'))
    else:
        raise PermissionDenied(_('Access denied'))


#отдать/забрать свой голос
@verified_email_required
def disvote(request, idea_id, condominium_slug):
    if(request.user.is_authenticated() and request.user.is_active):
        idea = get_object_or_404(Ideas, id=idea_id)
        if idea.condominium in request.user.condominiums.all():
            vote = get_object_or_404(IdeasVoices,idea=idea_id, user= request.user.id)
            vote.delete()
            #Karma.add(request.user,KARMA['PETITION_DISVOTE'],"Забрано голос з ідеї", "Ідеї")
            return redirect('../../ideas/%s' % idea_id)
        else:
            raise PermissionDenied(_('Access denied'))
    else:
        raise PermissionDenied(_('Access denied'))

#проверяем голосовал ли пользователь за петицию
def _getusersign(request, idea_id):

    if(request.user in [ p.user for p in IdeasVoices.objects.filter(idea = idea_id)]):
        return True
    else:
        return False


def print(request, idea_id, condominium_slug):
       idea = get_object_or_404(Ideas,id=idea_id)
       condominium = Condominium.objects.get(id=request.session['condominium_id'])
       idea_number = condominium.ideas_number_templ % (idea_id)
       condominium = Condominium.objects.get(id=request.session['condominium_id'])
       need_votes =  condominium.votes
       ideas_days = condominium.ideas_days
       if request.user.is_authenticated():
          allowed = request.user.isAllowedToModerate(idea.condominium.id, 'Ideas')
       else:
          allowed = False

       days_end = False
       if (idea.status.id == 5):
           date_start = idea.when_approve
           days_end = date_start + datetime.timedelta(days=ideas_days)
           day_now = datetime.datetime.now()

       if allowed:
           votes = IdeasVoices.objects.filter(idea=idea_id).exclude(block=1).all()
           owner = get_object_or_404(User,id = idea.owner_user.id)
           return render(request, 'idea_print.html',{'idea': idea,'needvotes': need_votes, 'owner': owner,'idea_number': idea_number,'allowed': allowed, 'votes': votes, 'end_date':days_end})
       else:
           raise PermissionDenied(_('Access denied.'))

def test(request, condominium_slug):
    ActivityMail.sendToModers(request,_('Test email'), 'new_idea.email', 1, {'url':'www.google.com','title': 'Сайт гугла'})
    return HttpResponse("Done!")
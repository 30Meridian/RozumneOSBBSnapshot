import datetime

from django.views.generic import DetailView, ListView, RedirectView
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from stronghold.decorators import public
from stronghold.views import StrongholdPublicMixin

from system.settings import CRON_SECRET
from polls.models import Choice, Poll, Vote


class PollListView(StrongholdPublicMixin, ListView):

    def get_queryset(self):
        if 'condominium_id' in self.request.session:
            if self.request.user.is_authenticated() and self.request.session['condominium_id'] in self.request.user.condominiums_list():
                return Poll.objects.filter(active=1, condominium=self.request.session['condominium_id']).order_by('id','archive')
            else:
                return Poll.objects.filter(active=1, condominium=self.request.session['condominium_id'],
                                           condominium__public_polls=1, public=1).order_by('id','archive')
        else:
            return Poll.objects.filter(active=1,  public=1)


class PollDetailView(StrongholdPublicMixin, DetailView):
    model = Poll

    def get_object(self):
        object = super(PollDetailView, self).get_object()
        if not (self.request.user.is_authenticated() and
                self.request.session['condominium_id'] in self.request.user.condominiums_list()) and \
                not (object.public and object.condominium.public_polls):
            raise PermissionDenied(_("Access denied"))
        return object

    def get_context_data(self, **kwargs):
        context = super(PollDetailView, self).get_context_data(**kwargs)

        if not 'condominium_id' in self.request.session:
            self.request.session['condominium_id'] = self.object.condominium.id
            self.request.session['condominium_name'] = self.object.condominium.name
            self.request.session['condominium_slug'] = self.object.condominium.slug

        if(self.request.user.is_authenticated() and self.request.user.is_active):
            context['poll'].votable = self.object.can_vote(self.request.user)
        else:
            context['poll'].votable = False

        return context


class PollVoteView(RedirectView):
    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(id=kwargs['pk'])
        user = request.user
        choice = Choice.objects.get(id=request.POST['choice_pk'])
        Vote.objects.create(poll=poll, user=user, choice=choice)
        messages.success(request,_("Thank, for your voice"))
        return redirect(reverse('condominium:polls:detail',kwargs={
            'condominium_slug': request.session['condominium_slug'],
            'pk': kwargs['pk']}))
        #return super(PollVoteView, self).post(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return redirect('../polls', args=[kwargs['pk']])

#проверяем кроном просроченые голосования и переносим в архивные
def checktimeout(request, secret, condominium_slug):
    if(secret == CRON_SECRET):
       polls = Poll.objects.filter(active=1, archive=0)
       count = 0
       for poll in polls:
           if(poll.date_end <= datetime.date.today() ):
               poll.archive= 1 # делаем архивной если у петиции кончилось время сбора подписей и она не набрала нужного количества голосов
               poll.save()
               count +=1
       if(count):
           return HttpResponse(_('Done! Find: ')+str(count)+_(' poll(-s)'))
       else:
           return HttpResponse(_("Not found any polls that mutch enddate!"))
    else:
        raise PermissionDenied(_('Access denied.'))
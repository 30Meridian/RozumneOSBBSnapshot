from .models import *
from django.shortcuts import get_object_or_404, redirect
from ipware.ip import get_ip
from defects.models import Condominium
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Q
from system.settings import DEFAULT_FROM_EMAIL
from email.header import Header


class Activity:
    '''Клас реализует запись всех процессов происходящих над петицией'''

    def add(self,request, idea_id, act_text):

            activity = IdeasActivity()
            user = get_object_or_404(User, id =request.user.id)
            idea = get_object_or_404(Ideas, id = idea_id)
            try:
                activity.user = user
                activity.idea = idea
                activity.activity = act_text
                activity.ip = self._ip(request)
                activity.save()

                return redirect('ideas:idea', arg=(idea_id))
            except:
                return False

    def add_robot(self,request, idea_id, act_text):

            activity = IdeasActivity()
            user = get_object_or_404(User, id =request.user.id)
            idea = get_object_or_404(Ideas, id = idea_id)
            try:
                activity.user = user
                activity.idea = idea
                activity.activity = act_text
                activity.ip = self._ip(request)
                activity.save()

                return True
            except:
                return False



    def _ip(self,request):
        '''Получаем IP клиента с request'''
        ip = get_ip(request)
        if ip is not None:
            return ip
        else:
            return 'local'

class ActivityMail:
    '''Отправляем почту на основе темплейтов'''
    def sendToModers(request, subject, template_name, condominium, context,email=None, module='Ideas'):
        recipients = []
        if(email == None):
            recipients = []
            users = Condominium.objects.get(pk=int(condominium)).user_set.filter(Q(groups__name='Moderator_%s' % module ) | Q(groups__name='Moderator'))
            for user in users:
                recipients.append(user.email)
        else:
            recipients = email

        template_html = render_to_string('emails/'+template_name, context)
        template_plain = render_to_string('emails/'+template_name, context)

        send_mail(
            subject,
            template_plain,
            DEFAULT_FROM_EMAIL,
            recipients,
            html_message=template_html,
        )
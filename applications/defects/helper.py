from .models import *
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Q
from system.settings import DEFAULT_FROM_EMAIL


class ActivityMail:
    '''Отправляем почту на основе темплейтов'''
    def sendToModers(request, subject, template_name, condominium, context, email=None, module='Defects'):
        recipients = []
        if(email == None):
            recipients = []
            users = Condominium.objects.get(pk=int(condominium)).user_set.filter(Q(groups__name='Moderator_%s' % module ) | Q(groups__name='Moderator') | Q(groups__name='Control_%s' % module ))
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

    #sending emails to all subcontractor's users
    def sendToSubcontractors(request, subject, template_name, subcontractor, context ):

        recipients = [user.email for user in Subcontractors.objects.get(pk=subcontractor).user_set.all()]

        template_html = render_to_string('emails/'+template_name, context)
        template_plain = render_to_string('emails/'+template_name, context)

        send_mail(
            subject,
            template_plain,
            DEFAULT_FROM_EMAIL,
            recipients,
            html_message=template_html,
        )
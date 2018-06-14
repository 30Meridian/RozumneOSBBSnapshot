import re

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


class UserRequiredMiddleware(object):
    """
        Check if user is registered in current condominium.
        If user is not member in current condominium, class locks some urls and such activities as create, update, delete in this condominium.
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.user.is_authenticated():
                if request.session['condominium_id'] in request.user.condominiums_list() or \
                        self.is_public_url(request):
                    return None
                else:
                    messages.error(request, _('You have not permission to change anything in this condominium!'))
                    return redirect(reverse('condominium:home', args=[request.session['condominium_slug']]))
            return None
        except:
            return None

    def is_public_url(self, request):
        cur_url = request.path_info
        public_urls = self.public_urls_list(request)
        return any([re.match(url, cur_url) for url in public_urls])

    def public_urls_list(self, request):
        slug = request.session['condominium_slug']
        public_urls = [
            r'^/condominium/{slug}/home$',
            r'^/condominium/{slug}/$',
            r'^/condominium/{slug}/news/$',
            r'^/condominium/{slug}/ideas/$',
            r'^/condominium/{slug}/ideas/status/2$',
            r'^/condominium/{slug}/ideas/status/5$',
            r'^/condominium/{slug}/polls/$',
            r'^/condominium/{slug}/problems/list$',
            r'^/condominium/{slug}/news/\d+$',
            r'^/condominium/{slug}/ideas/\d+$',
            r'^/condominium/{slug}/polls/\d+$',
            r'^/condominium/{slug}/problems/\d+$',

            r'^/$',
            r'^/jsi18n/$',
            r'^/condominiumactivesearch$',
            r'^/media/',
            r'^/static/',
            r'^/search/',
            r'^/help/$',
            r'^/contacts$',
            r'^/about/$',
            r'^/instructions/$',
            r'^/accounts/logout',
            r'^/profile/\d+$',
            r'^/profile/\d+/edit/$',
            r'^/profile/\d+/condominium-update/$',
            r'^/filter-cities$',
            r'^/filter-condominiums',
            r'^/profile/\d+/add_non_residence/$',
            r'^/delete_residence/\d+$',
            r'^/delete_non_residence/\d+$',
            r'^/profile/\d+/add_residence/$',
            r'^/index',
            r'^/manage',

        ]

        return [url.format(slug=slug) for url in public_urls]

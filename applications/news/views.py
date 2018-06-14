from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# from .forms import NewsAdd
from django.core.exceptions import PermissionDenied
from allauth.account.decorators import verified_email_required
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

from stronghold.decorators import public

from system.models import Condominium
from .models import News

# Отобразить список новостей
@public
def list(request, condominium_slug):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    if 'condominium_id' in request.session:
        allowed = False
        if request.user.is_authenticated() and request.session['condominium_id'] in request.user.condominiums_list():
            news_list = News.objects.filter(condominium=request.session['condominium_id'], publish=1,
                                            datetime_publish__lte=datetime.now).order_by('-datetime_publish')
        else:
            news_list = News.objects.filter(condominium=request.session['condominium_id'],
                                            publish=1, public=1, condominium__public_news=1,
                                            datetime_publish__lte=datetime.now).order_by('-datetime_publish')
        p = Paginator(news_list, 10, request=request)
        articles = p.page(page)
        return render(request, 'articles_list.html', {'articles': articles, 'allowed': allowed})
    else:
        return redirect(reverse('regions'))


# Отобразить новость
@public
def article(request, id, condominium_slug):
    article = get_object_or_404(News, id=id)

    if not 'condominium_id' in request.session:
        request.session['condominium_id'] = article.condominium.id
        request.session['condominium_name'] = article.condominium.name
        request.session['condominium_slug'] = article.condominium.slug

    allowed = False

    if (article.publish == False and allowed == False):
        raise PermissionDenied(_("Access denied"))

    if not (request.user.is_authenticated() and
            request.session['condominium_id'] in request.user.condominiums_list()) and \
            not (article.public and article.condominium.public_news):
        raise PermissionDenied(_("Access denied"))

    return render(request, 'article.html', {'article': article, 'allowed': allowed, })


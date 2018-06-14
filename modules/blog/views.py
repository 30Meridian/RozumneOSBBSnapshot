
import system
import datetime
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied

from haystack.generic_views import SearchView
from photologue.models import Photo, Gallery
from system.models import User, Condominium

from .models import Articles, Like, Category


def index(request):
    api_key = system.settings.GOOGLE_API_KEY
    condominiums = Condominium.objects.all()
    photos = Photo.objects.all().order_by('-date_added')[:3]

    articles = Articles.objects.filter(datetime_publish__lte=datetime.datetime.now, publish=1). \
                   order_by("-datetime_publish")

    first_article = articles[0]
    second_article = articles[1]

    articles = articles[2:]

    size = len(articles)
    half1_articles = articles[:size//2+1]
    half2_articles = articles[size//2+1:]

    photos_info = []
    for photo in photos:
        gallery = photo.public_galleries().first()
        photos_info.append({'photo': photo, 'gallery': gallery})
    return render(request, 'blog/index.html',
                  context={
                      'half1_articles': half1_articles,
                      'half2_articles': half2_articles,
                      'first_article': first_article,
                      'second_article': second_article,
                      'articles': articles,
                      'condominiums': condominiums,
                      'api_key': api_key,
                      'photos_info': photos_info
                  })


def articles_list(request, category_slug=None):
    category_title = None
    if category_slug:
        all_articles = Articles.objects.filter(
            datetime_publish__lte=datetime.datetime.now, publish=1,
            categories__slug=category_slug).order_by("-datetime_publish")
        category_title = Category.objects.get(
            slug=category_slug
        ).title

    else:
        all_articles = Articles.objects.filter(datetime_publish__lte=datetime.datetime.now, publish=1).\
            order_by("-datetime_publish")
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p_articles = Paginator(all_articles, 10, request=request)
    articles = p_articles.page(page)

    return render(request, 'blog/articles_list.html',
                  context={
                      'articles': articles,
                      'category_title': category_title
                  })


def article_detail(request, id):
    likes_count = Like.objects.filter(article__id=id).count
    try:
        current_user_like = Like.objects.get(article__id=id, user=request.user)
    except:
        current_user_like = False

    articles = Articles.objects.filter(datetime_publish__lte=datetime.datetime.now, publish=1).\
                   order_by("-datetime_publish")[:3]
    try:
        article = Articles.objects.get(
            id=id, publish=1, datetime_publish__lte=datetime.datetime.now)
        photos = article.photo_set.all()
    except:
        return render(request, 'blog/404.html')

    return render(request, 'blog/article.html',
                  context={
                      'article': article,
                      'articles': articles,
                      'photos': photos,
                      'likes_count': likes_count,
                      'user_like': current_user_like,
                  })


@csrf_exempt
def like_article(request):
    user = User.objects.get(id=request.POST.get('user_id'))
    article = Articles.objects.get(id=request.POST.get('article_id'))
    try:
        Like.objects.get(user=user, article=article).delete()
    except:
        Like.objects.create(user=user, article=article)
    return HttpResponse('OK')


def last_grants(request):
    pass


def about_us(request):
    try:
        article = Articles.objects.get(categories__slug='about')
        return render(request, 'blog/static.html',context={'article':article})
    except:
        return render(request, 'blog/about.html')


def contacts(request):
    api_key = system.settings.GOOGLE_API_KEY
    return render(request, 'blog/contact.html',
                  context={'api_key': api_key})


def team(request):
    return render(request, 'blog/team.html')


def get_news(date, days_count):
    from news.models import News
    query = News.objects.filter(publish=True, datetime_publish__lt=date,
                                public=True, condominium__public_news=True).order_by('-datetime_publish')
    if days_count is not None:
        end_date = date - datetime.timedelta(days=days_count)
        query = query.filter(datetime_publish__gt=end_date)

    result = []
    for news in query[0:10]:
        try:
            image_url = news.mainimg.url
        except ValueError:
            image_url = ''

        result.append({
            'type': 2,
            'id': news.id,
            'datetime': news.datetime_publish,
            'time': news.datetime_publish.time(),
            'class': 'fa fa-newspaper-o bg-green',
            'town_name': news.condominium.name,
            'town_slug': news.condominium.slug,
            'module_name': 'Новини',
            'module_link': 'news/',
            'image': image_url,
            'header': news.title,
            'content': news.shortdesc or ''
        })

    return result


def get_ideas(date, days_count):
    from ideas.models import Ideas
    query = Ideas.objects.filter(status__in=[2, 4, 6], when_approve__lt=date,
                                 public=True, condominium__public_ideas=True).order_by('-when_approve')
    if days_count is not None:
        end_date = date - datetime.timedelta(days=days_count)
        query = query.filter(when_approve__gt=end_date)


    result = []
    for idea in query[0:10]:
        try:
            image_url = idea.image.url
        except ValueError:
            image_url = ''

        result.append({
            'type': 2,
            'id': idea.id,
            'datetime': idea.when_approve,
            'time': idea.when_approve.time(),
            'class': 'fa fa-commenting-o bg-blue',
            'town_name': idea.condominium.name,
            'town_slug': idea.condominium.slug,
            'module_name': 'Ідеї',
            'module_link': 'ideas/',
            'image': image_url,
            'status': str(idea.status),
            'header': idea.title,
            'content': idea.text or ''
        })

    return result


def get_problems(date, days_count):
    from problems.models import Items
    query = Items.objects.filter(create__lt=date,public=True,
                                 condominium_ref__public_problems=True).order_by('-create')
    if days_count is not None:
        end_date = date - datetime.timedelta(days=days_count)
        query = query.filter(create__gt=end_date)


    result = []
    for item in query[0:10]:
        try:
            image_url = item.photo.url
        except ValueError:
            image_url = ''
        try:
            status = str(item.problems_items.all().order_by('-create')[0])
        except IndexError:
            status = ''
        result.append({
            'type': 2,
            'id': item.id,
            'datetime': item.create,
            'time': item.create.time(),
            'class': 'fa fa-commenting-o bg-blue',
            'town_name': item.condominium_ref.name,
            'town_slug': item.condominium_ref.slug,
            'module_name': 'Проблеми',
            'module_link': 'problems/',
            'image': image_url,
            'status': status,
            'header': item.title,
            'content': item.description or ''
        })

    return result


def get_polls(date, days_count=None):
    from polls.models import Poll

    query = Poll.objects.filter(date_start__lte=date, public=True,
                                condominium__public_polls=True).order_by('-date_start')
    if days_count is not None:
        end_date = date - datetime.timedelta(days=days_count)
        query = query.filter(date_start__gte=end_date)

    result = []
    for poll in query[0:10]:
        result.append({
            'type': 2,
            'id': poll.id,
            'datetime': datetime.datetime.combine(poll.date_start, datetime.datetime.min.time()),
            'time':  '',
            'class': 'fa  fa-check bg-orange',
            'town_name': poll.condominium.name,
            'town_slug': poll.condominium.slug,
            'module_name': 'Опитування',
            'module_link': 'polls/',
            'header': poll.question,
            'content': poll.description or ''
        })
    return result


def get_new_day(date):
    return {
        'type': 1,
        'date': date.date()
    }


def live_stream_list(date, filter_list=None, days_count=None):
    date = date + datetime.timedelta(hours=2)
    related_func = {
        'News': get_news,
        'Ideas': get_ideas,
        'Polls': get_polls,
        'Problems': get_problems
    }

    object_list = []
    for tag in filter_list:
        objects = related_func[tag](date, days_count)
        if len(objects):
            object_list.append(objects)

    last_datetime = date
    result = []
    for post in range(10):
        if len(object_list) == 0:
            result.append({'type': 3})
            break
        else:
            max_val = object_list[0][0]['datetime']
            max_index = 0
            if len(object_list) > 1:
                for i in range(1, len(object_list)):
                    if object_list[i][0]['datetime'] > max_val:
                        max_val = object_list[i][0]['datetime']
                        max_index = i

        present_datetime = object_list[max_index][0]['datetime']
        if present_datetime.date() < last_datetime.date():
            result.append(get_new_day(present_datetime))
        last_datetime = present_datetime

        result.append(object_list[max_index].pop(0))
        if len(object_list[max_index]) == 0:
            object_list.pop(max_index)

    return {'value': result, 'end_date': last_datetime.isoformat()}


@csrf_exempt
def last_news(request):
    date = datetime.datetime.strptime(request.GET['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
    filter_list = ['News', 'Ideas', 'Polls', 'Problems']  # it will be sent from user later

    return JsonResponse(live_stream_list(date, filter_list), safe=False)


@csrf_exempt
def popular_category(request):
    result = []
    for category in Category.objects.all():
        categories = {}
        if not category.slug=='about':
            categories['title'] = category.title
            categories['slug'] = category.slug
            result.append(categories)

    return JsonResponse(result, safe=False)


@csrf_exempt
def grants(request):
    result = []
    for article in Articles.objects.filter(categories__slug='grants', publish=1).order_by("-datetime_publish"):
        artcs = {}

        artcs['title'] = article.title
        artcs['author_art'] = article.author.get_full_name()
        artcs['date'] = article.datetime_publish.date()
        artcs['image'] = article.mainimg.thumbnail.url
        artcs['article_id'] = article.id

        result.append(artcs)

    return JsonResponse(result, safe=False)


def best_practice(request):
    return render(request, 'blog/best_practice.html')


def partners(request):
    return render(request, 'blog/partners.html')


class CustomSearchView(SearchView):
    template_name = 'blog/search/search_articles.html'

    def get(self, request, *args, **kwargs):
        context = super(CustomSearchView, self).get(request, *args, **kwargs)
        return context


search_articles = CustomSearchView.as_view()
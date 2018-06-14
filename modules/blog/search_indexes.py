import datetime

from haystack import indexes

from .models import Articles


class ArticlesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    author = indexes.CharField(model_attr='author')
    shortdesc = indexes.CharField(model_attr='shortdesc')
    title = indexes.CharField(model_attr='title')

    def get_model(self):
        return Articles

    def index_queryset(self, using=None):
        return self.get_model().objects.exclude(publish=0)


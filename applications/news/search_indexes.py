from .models import News
from haystack import indexes
# Only for testing purposes


class NewIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author= indexes.CharField(model_attr='author')
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='text')
    condominium = indexes.CharField(model_attr='condominium__slug')

    def get_model(self):
        return News

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.filter(publish=True)

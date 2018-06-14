from .models import Ideas
from haystack import indexes
# Only for testing purposes
from haystack.query import SearchQuerySet

class IdeaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='text')
    condominium = indexes.CharField(model_attr='condominium__slug')


    def get_model(self):
        return Ideas

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.all()




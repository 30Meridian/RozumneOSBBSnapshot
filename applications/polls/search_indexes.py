from .models import Poll
from haystack import indexes
# Only for testing purposes


class PollIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='question')
    content = indexes.CharField(model_attr='description')
    condominium = indexes.CharField(model_attr='condominium__slug')

    def get_model(self):
        return Poll

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.all()

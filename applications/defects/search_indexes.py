from .models import  Issues
from haystack import indexes
# Only for testing purposes


class IssuesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    content= indexes.CharField(model_attr='description')
    owner_ref = indexes.CharField(model_attr='owner_ref')
    condominium = indexes.CharField(model_attr='condominium_ref__slug')

    def get_model(self):
        return Issues

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.all()

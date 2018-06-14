from .models import User
from haystack import indexes
# Only for testing purposes


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    first_name = indexes.CharField(model_attr='first_name')
    middle_name = indexes.CharField(model_attr='middle_name')
    last_name = indexes.CharField(model_attr='last_name')
    phone = indexes.CharField(model_attr='phone')
    # email = indexes.CharField(model_attr='email')
    condominium = indexes.CharField()

    def prepare_condominium(self, obj):
        return [cond.slug for cond in obj.condominiums.all()]

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.all()

from django.utils.translation import ugettext_lazy as _


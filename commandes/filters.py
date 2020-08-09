
from django_filters import FilterSet, ModelMultipleChoiceFilter
from .models import Commandes

class CommandesFilter(FilterSet):
    
    class Meta:
        model = Commandes
        fields = {'numero_commande'}


from django_filters import FilterSet, ModelChoiceFilter, ChoiceFilter
from .models import Commandes
from utilisateurs.models import User
from django.db.models import Q

STATUS_CHOICES = (
    (1, 'Non payé'),
    (2, 'Payé'),
    (3, 'En transit'),
    (4, 'En agence'),
    (5, 'Livré'),
    (6, 'Réceptionné'),
)


class CommandesFilter(FilterSet):
    colis__client = ModelChoiceFilter(queryset=User.objects.exclude(Q(user_type=1) | Q(user_type=2)| Q(user_type=3)))
    driver = ModelChoiceFilter(queryset=User.objects.filter(user_type=3))
    status = ChoiceFilter(choices=STATUS_CHOICES)

    class Meta:
        model = Commandes
        fields = { 'numero_commande', 'colis__client', 'price', 'driver', 'status'}


class CommandesClientFilter(FilterSet):
    status = ChoiceFilter(choices=STATUS_CHOICES)

    class Meta:
        model = Commandes
        fields = { 'numero_commande', 'price', 'status'}


class CommandesDriverFilter(FilterSet):
    STATUS_CHOICES = (
        (3, 'En transit'),
        (4, 'En agence'),
        (5, 'Livré'),
        (6, 'Réceptionné'),
    )
    status = ChoiceFilter(choices=STATUS_CHOICES)

    class Meta:
        model = Commandes
        fields = { 'numero_commande', 'city_depart', 'city_arrive', 'status'}
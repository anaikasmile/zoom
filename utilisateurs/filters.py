import django_filters
from .models import User, Person

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'username']
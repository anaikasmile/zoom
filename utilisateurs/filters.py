import django_filters
from .models import User

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['last_name', 'first_name']
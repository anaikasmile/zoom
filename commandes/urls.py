from django.urls import path
from . import views

app_name = 'commandes'
urlpatterns = [
    path('', views.home, name='home'),
    path('commandes/create', views.ColisCreateView.as_view(), name='create_commande'),

]
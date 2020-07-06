from django.urls import path
from . import views

app_name = 'commandes'
urlpatterns = [
    path('', views.home, name='home'),
    path('commandes/ajouter', views.ColisCreateView.as_view(), name='create_commande'),
    path('commandes/liste', views.commandes_liste, name='liste_commandes'),
    path('commandes/disponibles', views.avalaible_orders, name='avalaible_orders'),

    path('ajax/update/etat/', views.etat_update, name='update_etat'),
    path('ajax/assign/', views.assign_order_to_me, name='assign_order_to_me'),

    path('commandes/historiques/<int:commande_id>/', views.historique_commande, name='historique_commande'),

    path('mes-commandes/', views.mes_commandes, name='mes_commandes'),
    path('mes-commandes-detail/<int:commande_id>/', views.mes_commandes_detail, name='mes_commandes_detail'),

    path('commandes/reclamation/ajouter', views.add_reclamation, name='add_reclamation'),

]
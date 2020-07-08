from django.urls import path
from . import views

app_name = 'commandes'
urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/commandes/liste', views.commandes_liste, name='liste_commandes'),
    path('ajax/update/etat/', views.etat_update, name='update_etat'),
    path('commandes/historiques/<int:commande_id>/', views.historique_commande, name='historique_commande'),

    #frontend
    path('commandes/creer', views.ColisCreateView.as_view(), name='create_commande'),
    path('commandes/', views.mes_commandes, name='mes_commandes'),
    path('commandes/<int:commande_id>/', views.mes_commandes_detail, name='mes_commandes_detail'),
    path('commandes/disponibles', views.avalaible_orders, name='avalaible_orders'),
    path('ajax/commandes/assigner/', views.assign_order_to_me, name='assign_order_to_me'),

    path('reclamations/', views.add_reclamation, name='add_reclamation'),

]
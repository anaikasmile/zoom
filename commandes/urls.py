from django.urls import path
from . import views

app_name = 'commandes'
urlpatterns = [

    path('stats/', views.stats, name='dashboard'),
    path('dashboard/commandes/liste', views.commandes_liste, name='liste_commandes'),
    path('ajax/update/etat/', views.etat_update, name='update_etat'),

    #frontend
    path('', views.home, name='home'),

    path('commandes/creer', views.ColisCreateView.as_view(), name='create_commande'),
    path('commandes/', views.mes_commandes, name='mes_commandes'),
    path('commandes/<int:commande_id>/', views.mes_commandes_detail, name='mes_commandes_detail'),
    path('commandes/disponibles', views.avalaible_orders, name='avalaible_orders'),
    path('commandes/delivres', views.delivery_orders_by_driver, name='unavalaible_orders'),
    path('commandes/historiques/<int:commande_id>/', views.historique_commande, name='historique_commande'),

    path('ajax/commandes/assigner/', views.assign_order_to_me, name='assign_order_to_me'),

    path('reclamations/', views.add_reclamation, name='add_reclamation'),
    path('ajax/reclamations/handler/<int:cmd_id>', views.handler_reclamation_cmd, name='handler_reclamation_cmd'),

]
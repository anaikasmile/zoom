from django.urls import path
from . import views

app_name = 'commandes'
urlpatterns = [

    path('dashboard/', views.stats, name='dashboard'),
    path('dashboard/commandes/liste', views.commandes_liste, name='liste_commandes'),
    path('ajax/update/etat/', views.etat_update, name='update_etat'),
    path('dashboard/reclamations/liste', views.list_reclamation, name='liste_reclamations'),
    path('dashbord/commandes/historiques/<int:commande_id>/', views.historique_commande_admin, name='historique_commande_admin'),
    path('dashboard/commandes/<int:commande_id>', views.commande_view, name='commande_view'),

    path('dashboard/tranches/create', views.tranche_create, name='tranche_create'),
    path('dashboard/tranches/update/<int:tranche_id>/', views.tranche_update, name='tranche_update'),
    path('dashboard/tranches/delete/<int:tranche_id>/', views.tranche_delete, name='tranche_delete'),
    path('dashboard/package/create', views.package_create, name='package_create'),
    path('dashboard/package/update/<int:package_id>/', views.package_update, name='package_update'),
    path('dashboard/package/delete/<int:package_id>/', views.package_delete, name='package_delete'),

    #frontend
    path('', views.home, name='home'),

    path('commandes/creer', views.commande_create, name='create_commande'),
    path('commandes/', views.mes_commandes, name='mes_commandes'),
    path('commandes/<commande_ref>/', views.mes_commandes_detail, name='mes_commandes_detail'),
    path('commandes/detail/<commande_ref>/', views.commande_view_driver, name='commande_detail_driver'),

    path('commandes/disponibles', views.avalaible_orders, name='avalaible_orders'),
    path('commandes/delivres', views.delivery_orders_by_driver, name='unavalaible_orders'),
    path('commandes/historiques/<commande_ref>/', views.historique_commande, name='historique_commande'),

    path('ajax/commandes/assigner/', views.assign_order_to_me, name='assign_order_to_me'),

    path('reclamations/', views.add_reclamation, name='add_reclamation'),
    path('ajax/reclamations/handler/<int:cmd_id>', views.handler_reclamation_cmd, name='handler_reclamation_cmd'),

    path('facture/<commande_ref>', views.generate, name='generate_facture'),

    

]
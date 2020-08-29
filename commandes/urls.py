from django.urls import path
from . import views

app_name = 'commandes'
urlpatterns = [

    path('dashboard/', views.stats, name='dashboard'),
    path('liste/', views.CommandesListView.as_view(), name='liste'),

    path('admin/commandes/liste', views.CommandesListView.as_view(), name='liste_commandes'),

    path('ajax/update/etat/', views.etat_update, name='update_etat'),
    path('admin/reclamations/liste/', views.list_reclamation, name='liste_reclamations'),
    path('admin/reclamations/handler/', views.add_handler_reclamation_cmd, name='handler_reclamation_cmd'),
    path('admin/reclamations/handler/<int:commande_id>', views.add_handler_reclamation_cmd, name='handler_reclamation_cmd'),

    path('admin/commandes/historiques/<int:commande_id>/', views.historique_commande_admin, name='historique_commande_admin'),
    path('admin/commandes/<int:commande_id>', views.commande_view, name='commande_view'),

    path('admin/commissions', views.commissions, name='liste_commissions'),


    path('admin/tranches/create', views.tranche_create, name='tranche_create'),
    path('admin/tranches/update/<int:tranche_id>/', views.tranche_update, name='tranche_update'),
    path('admin/tranches/delete/<int:tranche_id>/', views.tranche_delete, name='tranche_delete'),
    path('admin/package/create', views.package_create, name='package_create'),
    path('admin/package/update/<int:package_id>/', views.package_update, name='package_update'),
    path('admin/package/delete/<int:package_id>/', views.package_delete, name='package_delete'),

    #frontend
    path('', views.home, name='home'),

    path('commandes/creer', views.commande_create, name='create_commande'),


    path('commandes', views.ClientCommandeListView.as_view(), name='mes_commandes'),
    path('commandes/chauffeurs', views.DriverCommandeListView.as_view(), name='drivers_orders'),
    path('commandes/disponibles/', views.AvailableCommandeListView.as_view(), name='availables_orders'),


    path('commandes/<commande_ref>/', views.mes_commandes_detail, name='mes_commandes_detail'),
    path('commandes/detail/<commande_ref>/', views.commande_view_driver, name='commande_detail_driver'),

    path('commandes/delivres', views.delivery_orders_by_driver, name='unavalaible_orders'),

    path('ajax/commandes/assigner/', views.assign_order_to_me, name='assign_order_to_me'),

    path('reclamations/', views.add_reclamation, name='add_reclamation'),

    path('facture/<commande_ref>', views.generate, name='generate_facture'),
    path('commande/recap/<commande_ref>', views.commande_recap, name='commande_recap'),

    

]
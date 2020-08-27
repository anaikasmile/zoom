from django.urls import path
from . import views as agence_views

app_name = 'agences'
urlpatterns = [
    path('agence/create', agence_views.agence_create, name='agence-create'),
    path('agence/update/<int:agence_id>/', agence_views.agence_update, name='agence-update'),
    path('agence/delete/<int:agence_id>/', agence_views.agence_delete, name='agence-delete'),
    path('agence/view/<int:agence_id>/', agence_views.agence_view, name='agence-view'),

    # path('vehicule/create', agence_views.vehicule_create, name='vehicule-create'),
    # path('vehicule/update/<int:vehicule_id>/', agence_views.vehicule_update, name='vehicule-update'),
    # path('vehicule/delete/<int:vehicule_id>/', agence_views.vehicule_delete, name='vehicule-delete'),
    # path('vehicule/detail/<int:vehicule_id>/', agence_views.vehicule_detail, name='vehicule-detail'),
    # path('vehicule/liste', agence_views.vehicule_list, name='vehicule-list'),

    # path('typevehicule/create', agence_views.type_vehicule_create, name='type-vehicule-create'),
    # path('typevehicule/update/<int:type_vehicule_id>/', agence_views.type_vehicule_update, name='type-vehicule-update'),
    # path('typevehicule/delete/<int:type_vehicule_id>/', agence_views.type_vehicule_delete, name='type-vehicule-delete'),

]
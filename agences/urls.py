from django.urls import path
from . import views as agence_views

app_name = 'agences'
urlpatterns = [
    path('create', agence_views.agence_create, name='agence-create'),
    path('update/<int:agence_id>/', agence_views.agence_update, name='agence-update'),
    path('delete/<int:agence_id>/', agence_views.agence_delete, name='agence-delete'),

    path('vehicule/create', agence_views.vehicule_create, name='vehicule-create'),
    path('vehicule/update/<int:vehicule_id>/', agence_views.vehicule_update, name='vehicule-update'),
    path('vehicule/delete/<int:vehicule_id>/', agence_views.vehicule_delete, name='vehicule-delete'),
    path('vehicule/detail/<int:vehicule_id>/', agence_views.vehicule_detail, name='vehicule-detail'),

    path('typevehicule/create', agence_views.type_vehicule_create, name='type-vehicule-create'),
    path('typevehicule/update/<int:type_vehicule_id>/', agence_views.type_vehicule_update, name='type-vehicule-update'),
    path('typevehicule/delete/<int:type_vehicule_id>/', agence_views.type_vehicule_delete, name='type-vehicule-delete'),

]
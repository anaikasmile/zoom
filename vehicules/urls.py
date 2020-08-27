from django.urls import path
from . import views as vehicule_views

app_name = 'vehicules'
urlpatterns = [

    path('create', vehicule_views.vehicule_create, name='vehicule-create'),
    path('update/<int:vehicule_id>/', vehicule_views.vehicule_update, name='vehicule-update'),
    path('delete/<int:vehicule_id>/', vehicule_views.vehicule_delete, name='vehicule-delete'),
    path('detail/<int:vehicule_id>/', vehicule_views.vehicule_detail, name='vehicule-detail'),
    path('liste', vehicule_views.vehicule_list, name='vehicule-list'),

    path('type/create', vehicule_views.type_vehicule_create, name='type-vehicule-create'),
    path('type/update/<int:type_vehicule_id>/', vehicule_views.type_vehicule_update, name='type-vehicule-update'),
    path('type/delete/<int:type_vehicule_id>/', vehicule_views.type_vehicule_delete, name='type-vehicule-delete'),

]
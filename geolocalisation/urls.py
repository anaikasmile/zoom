from django.urls import path
from . import views as place_views

app_name = 'geolocalisation'
urlpatterns = [
    path('city/create', place_views.city_create, name='city_create'),
    path('city/update/<int:city_id>/', place_views.city_update, name='city_update'),
    path('city/delete/<int:city_id>/', place_views.city_delete, name='city_delete'),
    path('district/create', place_views.district_create, name='district_create'),
    path('district/update/<int:district_id>/', place_views.district_update, name='district_update'),
    path('district/delete/<int:district_id>/', place_views.district_delete, name='district_delete'),
    #path('district/create', DistrictView.as_view(), name='add_district'),

]
from django.urls import path
from . import views as affectation_views

app_name = 'affectation'
urlpatterns = [
    path('create/<int:user_id>', affectation_views.affectation_create, name='affectation-create')
]
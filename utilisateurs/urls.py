from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'utilisateurs'
urlpatterns = [
	path('generate_password/', user_views.generate_password, name='generate_password'),

    path('registration/<int:role>/', user_views.registration, name='user_registration'),
    path('update/<int:user_id>/', user_views.user_update, name='user_update'),
    path('delete/<int:user_id>/', user_views.user_delete, name='user_delete'),
    path('password/change/<int:user_id>/', user_views.user_password_change, name='user_password_change'),


    path('signup/', user_views.signup, name='user_signup'),
    path('login/', user_views.user_login, name='login'),
    path('logout/', user_views.user_logout, name='logout'),

    path('liste/', user_views.UserListView.as_view(), name='user_list'),
    path('clients/', user_views.ClientListView.as_view(), name='user_client'),
    path('agents/', user_views.AgentListView.as_view(), name='user_agent'),
    path('drivers/', user_views.DriverListView.as_view(), name='user_driver'),
    path('view/<int:user_id>/', user_views.user_profile, name='user_profile'),


    


    path('profile', user_views.my_profile, name='my_profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.http import JsonResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, Group
from .models import Person, User, Identity
from .forms import UserForm, UserRegistrationForm, IdentityForm, PersonForm
from django.urls import reverse
from django.views.generic import ListView, CreateView
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.base_user import BaseUserManager
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .models import Person
from .tables import UserTable
from .filters import UserFilter
# Create your views here.

def generate_password(request):

    data = {
        'pwd': BaseUserManager().make_random_password(8),
    }
    return JsonResponse(data)


# Registration of user */
def registration(request,role):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        form_identity = IdentityForm(request.POST)

        if form.is_valid():
            user = form.save()

            user.refresh_from_db()  # load the profile instance created by the signal
            user.person.birth_date = form.cleaned_data.get('birth_date')
            user.person.tel = form.cleaned_data.get('tel')
            user.person.sexe = form.cleaned_data.get('sexe')
            user.person.adresse = form.cleaned_data.get('adresse')
            user.user_type = role
            user.save()
            identity = form_identity.save(commit=False)
            identity.user = user
            identity.save()

            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=user.username, password=raw_password)
            # login(request, user)
            return redirect('utilisateurs:user_registration', role)
    else:
        form = UserRegistrationForm()
        form_identity = IdentityForm()
    return render(request, 'utilisateurs/user_registration.html', {'form': form, 'form_identity': form_identity})

#Update User
def user_update(request,user_id):
    user = User.objects.get(id=user_id)
    identity = Identity.objects.get(user_id=user_id)
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST,request.FILES, instance=user)
        form_person = PersonForm(request.POST, request.FILES, instance=user.person)

        form_identity = IdentityForm(request.POST,request.FILES, instance=identity)

        if form.is_valid() and form_person.is_valid():
            form.save()
            form_person.save()           
            form_identity.save()
            messages.succes('Modification effectuée')
    else:
        form = UserRegistrationForm(instance=user)
        form_person = PersonForm(instance=user.person)
        form_identity = IdentityForm(instance=identity)
    return render(request, 'utilisateurs/user_update.html', {'form': form, 'form_person': form_person,'form_identity': form_identity})

# Registration of client */
def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.person.birth_date = form.cleaned_data.get('birth_date')
            user.person.tel = form.cleaned_data.get('tel')
            user.person.sexe = form.cleaned_data.get('sexe')
            user.person.adresse = form.cleaned_data.get('adresse')
            user.save()
            messages.success(request, 'Votre compte a été bien créé')

            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=user.username, password=raw_password)
            # login(request, user)
            return redirect('utilisateurs:user_signup')
    else:
        form = UserRegistrationForm()
    return render(request, 'utilisateurs/user_signup.html', {'form': form})

#Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            messages.success(request, 'Connexion réussie')
            return redirect('commandes:home')
        else:
            # testMot d'erreur
            messages.error(request, 'Identifiants invalides')
            return redirect('utilisateurs:login')

    return render(request, 'utilisateurs/user_login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Déconnexion réussie')
    return redirect('utilisateurs:login')


def my_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        form_person = PersonForm(request.POST, request.FILES, instance=request.user.person)

        if form.is_valid() and form_person.is_valid():
            form.save()
            form_person.save()
            messages.success(request, ('Votre profile a été mis à jour.'))
        else:
            messages.error(request, ('Certaines données sont incorecttes'))

        return HttpResponseRedirect("/users/myprofile")

    else:

        form = UserForm(instance=request.user)
        form_person = PersonForm(instance=request.user.person)
        #messages.error(request, ('Une erreur est survenue'))

    return render(request, 'utilisateurs/my_profile.html', {'form': form, 'form_person': form_person})


#####ADMIN
class UserListView(ListView):
    model = User
    # template_name = 'users/user_list.html'

class ClientListView(ListView):
    template_name = 'utilisateurs/clients.html'
    paginate_by = 10
    ordering = ['-created']
    def get_queryset(self):
        return User.objects.exclude(Q(user_type=1) | Q(user_type=2)|Q(user_type=3))

class AgentListView(SingleTableMixin, FilterView):
    table_class = UserTable
    template_name = "utilisateurs/user_list.html"
    filterset_class = UserFilter
    def get_queryset(self):
        return User.objects.filter(user_type=2)
# class AgentListView(ListView):
#     template_name = 'utilisateurs/user_list.html'
#     paginate_by = 10
#     ordering = ['-created']
#     def get_queryset(self):
#         return User.objects.filter(user_type=2)

class DriverListView(ListView):
    template_name = 'utilisateurs/user_list.html'
    paginate_by = 10
    ordering = ['lastname']
    def get_queryset(self):
        return User.objects.filter(user_type=3)


#Delete a user

def user_profile(request,user_id):
    user = get_object_or_404(User, id=user_id)

    context = {
            'user': user
    }

    return render(request, 'utilisateurs/user_profile.html', context)



def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'Utilisateur supprimé')
    return redirect('users:user-registration')
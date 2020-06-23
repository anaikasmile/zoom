from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, Group
from .models import Person, User
from .forms import UserForm, UserRegistrationForm, IdentityForm, PersonForm
from django.urls import reverse
from django.views.generic import ListView, CreateView
from django.db.models import Q
from django.contrib import messages


from .models import Person
# Create your views here.

# Registration of user */
def registration(request):
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
            user.save()
            identity = form_identity.save(commit=False)
            identity.user = user
            identity.save()

            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=user.username, password=raw_password)
            # login(request, user)
            return redirect('utilisateurs:user_registration')
    else:
        form = UserRegistrationForm()
        form_identity = IdentityForm()
    return render(request, 'utilisateurs/user_signup.html', {'form': form, 'form_identity': form_identity})


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

class UserListView(ListView):
    model = User
    # template_name = 'users/user_list.html'

class ClientListView(ListView):
    template_name = 'utilisateurs/user_list.html'
    paginate_by = 10
    ordering = ['-created']
    def get_queryset(self):
        return User.objects.exclude(Q(user_type=1) | Q(user_type=2)|Q(user_type=3))

class AgentListView(ListView):
    template_name = 'utilisateurs/user_list.html'
    paginate_by = 10
    ordering = ['-created']
    def get_queryset(self):
        return User.objects.filter(user_type=2)

class DriverListView(ListView):
    template_name = 'utilisateurs/user_list.html'
    paginate_by = 10
    ordering = ['-created']
    def get_queryset(self):
        return User.objects.filter(user_type=3)
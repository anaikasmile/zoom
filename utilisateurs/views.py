from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.http import JsonResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, Group
from .models import Person, User, Identity, Agent
from django.views.generic import ListView, CreateView
from django.db.models import Q, Count, F, Sum
from django.contrib.auth.base_user import BaseUserManager
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .models import Person
from agences.models import Agences
from .forms import AgentSignUpForm, UserForm, PersonForm, AgentForm, UserRegistrationForm, AgentRegistrationForm
from commandes.models import Commandes, Reclamations
from .tables import UserTable, ClientTable, DriverTable
from commandes.tables import CommandeClientTable, CommandeDriverTable
from .filters import UserFilter
# from django.contrib.auth.forms import PasswordChangeForm
from allauth.account.forms import ChangePasswordForm

# from formtools.wizard.views import SessionWizardView
# from django.core.files.storage import FileSystemStorage
# import os
# from django.conf import settings
from allauth.account.views import SignupView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.



def generate_password(request):

    data = {
        'pwd': BaseUserManager().make_random_password(8),
    }
    return JsonResponse(data)


# Registration of user */
def registration_agent(request):

    if request.method == 'POST':
        form = AgentRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            user.tel = form.cleaned_data.get('tel').as_e164
            user.save()
            type = form.cleaned_data['type']
            reference = form.cleaned_data['reference']
            initiated_at = form.cleaned_data['initiated_at']
            expired_at = form.cleaned_data['expired_at']
            contact_name = form.cleaned_data['contact_name']
            contact_tel = form.cleaned_data['contact_tel']
            photo = form.cleaned_data['photo']
            agence = form.cleaned_data['agence']
            agence = get_object_or_404(Agences, id=agence)
            agent = Agent.objects.create(user=user, type=type, reference=reference, initiated_at=initiated_at,
                expired_at=expired_at, contact_tel=contact_tel, contact_name=contact_name, photo=photo, agence=agence, is_agent=True)
            messages.success(request, 'Utilisateur créé')
            return redirect('utilisateurs:user_registration_agent')
    else:
        form = AgentRegistrationForm()
    return render(request, 'utilisateurs/user_registration_agent.html', {'form': form})


def registration_driver(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            user.tel = form.cleaned_data.get('tel').as_e164
            user.save()
            type = form.cleaned_data['type']
            reference = form.cleaned_data['reference']
            initiated_at = form.cleaned_data['initiated_at']
            expired_at = form.cleaned_data['expired_at']
            contact_name = form.cleaned_data['contact_name']
            contact_tel = form.cleaned_data['contact_tel']
            photo = form.cleaned_data['photo']
            agent = Agent.objects.create(user=user, type=type, reference=reference, initiated_at=initiated_at,
                expired_at=expired_at, contact_tel=contact_tel, contact_name=contact_name, photo=photo, is_driver=True)
            messages.success(request, 'Utilisateur créé')
            return redirect('utilisateurs:user_registration_driver')
    else:
        form = UserRegistrationForm()
    return render(request, 'utilisateurs/user_registration_driver.html', {'form': form})



# Registration of client */

def user_logout(request):
    logout(request)
    messages.success(request, 'Déconnexion réussie')
    return redirect('account_login')


def my_profile(request):

    try:
        getattr(request.user, 'agent')       

        table = CommandeDriverTable(Commandes.objects.filter(driver=request.user).order_by('created_at')[:10])
    except AttributeError:
        table = CommandeClientTable(Commandes.objects.filter(colis__client=request.user).order_by('created_at')[:10])


    context = {
            'form' : UserForm(instance=request.user),
            'form_person' : PersonForm(instance=request.user.person),
            'form_password' : ChangePasswordForm(request.user),
            'table' : table
        }
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        form_person = PersonForm(request.POST,  instance=request.user.person)


        if form.is_valid() and form_person.is_valid():
            form.save()
            form_person.save()
            messages.success(request, ('Votre profile a été mis à jour.'))
            return HttpResponseRedirect("/users/profile")
        else:
            messages.error(request, ('Certaines données sont incorecttes'))


    return render(request, 'utilisateurs/my_profile.html', context)


# #####ADMIN

class AgentSignupView(LoginRequiredMixin,SignupView):
    template_name = 'account/signup_agent.html'
    form_class = AgentSignUpForm
    redirect_field_name = 'next'
    success_url = None

   

class ClientListView(SingleTableMixin, FilterView):
    table_class = ClientTable
    filterset_class = UserFilter
    template_name = 'utilisateurs/clients.html'
    paginate_by = 25
    ordering = ['last_name']
    def get_queryset(self):
        return User.objects.filter(person__is_client=True)

class AgentListView(SingleTableMixin, FilterView):
    table_class = UserTable
    template_name = "utilisateurs/agents.html"
    paginate_by = 25
    filterset_class = UserFilter
    def get_queryset(self):
        return User.objects.filter(agent__is_agent=True)


class DriverListView(SingleTableMixin, FilterView):
    table_class = DriverTable
    template_name = 'utilisateurs/agents.html'
    paginate_by = 25
    filterset_class = UserFilter
    ordering = ['lastname']
    def get_queryset(self):
        return User.objects.filter(agent__is_driver=True)


# #View a user

def user_profile(request,user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        getattr(request.user, 'agent')  
        commandes = Commandes.objects.filter(driver=user)
        commission = Commandes.objects.filter(driver=user).filter(Q(status=Commandes.ETAT_RECEPTIONNE) | Q(status=Commandes.ETAT_LIVRE)).aggregate(Sum('commission'))
        reclamations = 0
    except AttributeError:
        
        commandes = Commandes.objects.filter(colis__client=user)
        commission = 0
    
        reclamations = Reclamations.objects.filter(commande__colis__client=user)

    nb_commandes = commandes.count()
    context = {
            'user': user,
            'nb_commandes': nb_commandes,
            'nb_reclamations': reclamations.count(),
            'total_commission': commission
    }

    return render(request, 'utilisateurs/user_profile.html', context)

# #Update User
def user_update(request,user_id):
    user = User.objects.get(id=user_id)
    identity = Agent.objects.get(user=user)
    if request.method == 'POST':
        form_person = UserForm(request.POST, request.FILES, instance=user)
        form_identity = AgentForm(request.POST,request.FILES, instance=identity)

        if form_person.is_valid() and form_identity.is_valid():
            form_person.save()           
            form_identity.save()
            messages.success(request,'Modification effectuée')
    else:
        form_person = UserForm(instance=user)
        form_identity = AgentForm(instance=identity)
    return render(request, 'utilisateurs/user_update.html', {'form_person': form_person,'form_identity': form_identity})


@login_required
def user_password_change(request, user_id):
    user = User.objects.get(id=user_id)
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user, request.POST)
            if form.is_valid():
               user = form.save()
               update_session_auth_hash(request, user)  # Important!
               messages.success(request, 'Mot de passe modifié')
               return redirect('utilisateurs:user_update user_id')
            else:
                messages.error(request, 'Données invalides')
        else:
            form = PasswordChangeForm(request.user)
    
        
    else:
        raise PermissionDenied

    return render(request, "utilisateurs/user_password_change.html", {
            "form": form
        })

#delete a user
@login_required
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        user.delete()
        messages.success(request, 'Utilisateur supprimé')

    except ProtectedError:

        messages.error(request, 'Suppression impossible')
    return redirect('utilisateurs:user-registration')

    
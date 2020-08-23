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
from .forms import UserForm, UserRegistrationForm, IdentityForm, PersonForm, ProfileInlineFormset, UserRegistrationForm1, UserRegistrationForm2
from django.views.generic import ListView, CreateView
from django.db.models import Q, Count, F, Sum
from django.contrib import messages
from django.contrib.auth.base_user import BaseUserManager
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .models import Person
from commandes.models import Commandes, Reclamations
from .tables import UserTable, ClientTable
from commandes.tables import CommandeClientTable, CommandeDriverTable
from .filters import UserFilter
from django.contrib.auth.forms import PasswordChangeForm
from allauth.account.forms import ChangePasswordForm

from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings


# Create your views here.

class FormWizardView(SessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))

    template_name = "utilisateurs/test.html"
    form_list = [UserRegistrationForm1, UserRegistrationForm2]
    def done(self, form_list, **kwargs):
        return render(self.request, 'done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })

def generate_password(request):

    data = {
        'pwd': BaseUserManager().make_random_password(8),
    }
    return JsonResponse(data)


# Registration of user */
def registration(request,role):

    if role == 1:
        name = 'Admin'
    elif role == 2:
        name = 'Agents'
    elif role == 3:
        name = "Chauffeurs"
    else: 
        name = "Clients"

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        form_identity = IdentityForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.person.birth_date = form.cleaned_data.get('birth_date')
            user.person.tel = form.cleaned_data.get('tel').as_e164
            user.person.sexe = form.cleaned_data.get('sexe')
            user.person.adresse = form.cleaned_data.get('adresse')
            user.user_type = role
            user.save()
            identity = form_identity.save(commit=False)
            identity.user = user
            identity.save()
            messages.success(request, 'Enregistement réussi')

            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=user.username, password=raw_password)
            # login(request, user)
            return redirect('utilisateurs:user_registration', role)
    else:
        form = UserRegistrationForm()
        form_identity = IdentityForm()
    return render(request, 'utilisateurs/user_registration.html', {'form': form, 'form_identity': form_identity, 'name': name})


# Registration of client */
def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.person.birth_date = form.cleaned_data.get('birth_date')
            user.person.tel = form.cleaned_data.get('tel').as_e164
            user.person.sexe = form.cleaned_data.get('sexe')
            user.person.adresse = form.cleaned_data.get('adresse')
            user.save()
            messages.success(request, 'Votre compte a été bien créé')
            login(request, user, backend='utilisateurs.AuthBackends.LoginBackend')

            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=user.username, password=raw_password)
            # login(request, user)
            return redirect('commandes:home')
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

    if request.user.user_type ==  3: #Si c'est un chauffeur
        table = CommandeDriverTable(Commandes.objects.filter(driver=request.user).order_by('created_at')[:10])
    else:
        table = CommandeClientTable(Commandes.objects.filter(colis__client=request.user).order_by('created_at')[:10])


    context = {
            'form' : UserForm(instance=request.user),
            'form_person' : PersonForm(instance=request.user.person),
            'form_password' : ChangePasswordForm(request.user),
            'table' : table
        }
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        form_person = PersonForm(request.POST, request.FILES, instance=request.user.person)


        if form.is_valid() and form_person.is_valid():
            form.save()
            form_person.save()
            messages.success(request, ('Votre profile a été mis à jour.'))
        else:
            messages.error(request, ('Certaines données sont incorecttes'))

        #return HttpResponseRedirect("/users/profile")

    
        #messages.error(request, ('Une erreur est survenue'))

    return render(request, 'utilisateurs/my_profile.html', context)


#####ADMIN
class UserListView(ListView):
    model = User
    # template_name = 'users/user_list.html'

class ClientListView(SingleTableMixin, FilterView):
    table_class = ClientTable
    filterset_class = UserFilter
    template_name = 'utilisateurs/clients.html'
    paginate_by = 25
    ordering = ['last_name']
    def get_queryset(self):
        return User.objects.exclude(Q(user_type=1) | Q(user_type=2)|Q(user_type=3))

class AgentListView(SingleTableMixin, FilterView):
    table_class = UserTable
    template_name = "utilisateurs/user_list.html"
    paginate_by = 25
    filterset_class = UserFilter
    def get_queryset(self):
        return User.objects.filter(user_type=2)


class DriverListView(SingleTableMixin, FilterView):
    table_class = UserTable
    template_name = 'utilisateurs/user_list.html'
    paginate_by = 25
    filterset_class = UserFilter
    ordering = ['lastname']
    def get_queryset(self):
        return User.objects.filter(user_type=3)


#View a user

def user_profile(request,user_id):
    user = get_object_or_404(User, id=user_id)
    if user.user_type == 3:
        commandes = Commandes.objects.filter(driver=user)
        commission = Commandes.objects.filter(driver=user).filter(Q(status=Commandes.ETAT_RECEPTIONNE) | Q(status=Commandes.ETAT_LIVRE)).aggregate(Sum('commission'))

    else:
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

#Update User
# def user_update(request,user_id):
#     user = User.objects.get(id=user_id)
#     try:
#         identity = Identity.objects.get(user_id=user_id)
#     except Identity.DoesNotExist:
#         identity = None

#     if request.method == 'POST':
#         form_person = PersonForm(request.POST, request.FILES, instance=user.person)
#         form_identity = IdentityForm(request.POST,request.FILES, instance=identity)

#         if form_person.is_valid():
#             form_person.save()           
#             form_identity.save()
#             messages.succes('Modification effectuée')
#     else:
#         form_person = PersonForm(instance=user.person)
#         form_identity = IdentityForm(instance=identity)
#     return render(request, 'utilisateurs/user_update.html', {'form_person': form_person,'form_identity': form_identity})

@login_required
def user_update(request, user_id):
    user = User.objects.get(id=user_id)
    
    try:
        identity = Identity.objects.get(user_id=user_id)
    except Identity.DoesNotExist:
        identity = None
    
 
    if request.user.is_authenticated:
        if request.method == "POST":
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)
            form_identity = IdentityForm(request.POST,request.FILES, instance=identity)
            if user_form.is_valid() and form_identity.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)
 
                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    form_identity.save()
                    messages.success('L utilisateur a été bien modifié')
        else:

            user_form = UserForm(instance=user)
            formset = ProfileInlineFormset(instance=user)
            form_identity = IdentityForm(instance=identity) 

        
    else:
        raise PermissionDenied

    return render(request, "utilisateurs/user_update.html", {
            "user_form": user_form,
            "formset": formset,
            "form_identity": form_identity,
            "user_id": user_id
        })

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

    
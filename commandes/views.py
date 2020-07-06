from django.shortcuts import render, reverse, get_object_or_404
from django.http import JsonResponse

from .models import Colis, Insurance, Commandes, HistoriqueCommandes
from agences.models import Agences
from .forms import CommandesForm, InsuranceForm, ColisForm, CommandesFormset, Step1Form, Step2Form,ReclamationForm
from django.views.generic import ListView, CreateView
from django.contrib import messages


import random
import string
# Create your views here.
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_order_id_generator(instance):
    reference = random_string_generator()

    Klass = instance.__class__

    qs_exists = Klass.objects.filter(numero_commande=reference).exists()
    if qs_exists:
        return unique_order_id_generator(instance)
    return reference

def home(request):

    return render(request, 'default/home.html', {})
    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Question.objects.order_by('-pub_date')[:5]


class ColisCreateView(CreateView):
    form_class = ColisForm
    template_name = 'commandes/create.html'
    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["commande"] = CommandesFormset(self.request.POST)
        else:
            data["commande"] = CommandesFormset()
        return data
    def form_valid(self, form):
        context = self.get_context_data()
        commande = context["commande"]
        self.object = form.save(commit=False)
        self.object.client = self.request.user
        self.object.save()
        if commande.is_valid():
            commande.instance = self.object
            commande.save()
            #reference = random_string_generator()
            # qs_exists = Commandes.objects.filter(numero_commande=reference).exists()
            # if qs_exists:
            #     reference = random_string_generator()
        return super().form_valid(form)
    def get_success_url(self):
        messages.success(self.request, 'Commande enregistrée')
        return reverse("commandes:create_commande")


def mes_commandes(request):
    commandes = Commandes.objects.filter(colis__client=request.user)
    #paginator = Paginator(agences, 25)  # Show 25  per page
    #page = request.GET.get('page')
    #agences = paginator.get_page(page)

    context = {
        'commandes': commandes,
    }
    return render(request, "commandes/mes_commandes.html", context)


def mes_commandes_detail(request,id):
    commande = get_object_or_404(Commandes, id=commande_id)

    #paginator = Paginator(agences, 25)  # Show 25  per page
    #page = request.GET.get('page')
    #agences = paginator.get_page(page)

    context = {
        'commande': commande,
    }
    return render(request, "commandes/mes_commandes_detail.html", context)

def commandes_liste(request):
    commandes = Commandes.objects.all()
    form_step1 = Step1Form
    form_step2 = Step2Form
    #paginator = Paginator(agences, 25)  # Show 25  per page
    #page = request.GET.get('page')
    #agences = paginator.get_page(page)

    context = {
        'commandes': commandes,
        'form_step1': form_step1,
        'form_step2': form_step2
    }
    return render(request, "commandes/commandes_liste.html", context)


#Liste des commandes disponibles
def avalaible_orders(request):
    commandes = Commandes.objects.filter(driver__isnull=True, status=Commandes.ETAT_PAYE)
    context = {
        'commandes': commandes
    }
    return render(request, "commandes/commandes_disponibles.html", context)


def etat_update(request):
    etat = request.GET.get('etat')
    cmd_id = request.GET.get('id')
    commande = get_object_or_404(Commandes, id=cmd_id)
    commande.status = etat
    commande.save()
    history = HistoriqueCommandes.objects.create(commande=commande, user=request.user, state=etat)
    if request.GET.get('agence'):
        agence = get_object_or_404(Agences, id=request.GET.get('agence'))
        history.agence = agence
        if request.GET.get('comment'):
            comment = request.GET.get('comment')
            history.comment = comment
    history.save()
    data = {
        'statut': 'success',
        'message': 'La commande a été mise à jour'
    }
    return JsonResponse(data)

def historique_commande(request,commande_id):
    commande = get_object_or_404(Commandes, id=commande_id)
    historiques = HistoriqueCommandes.objects.filter(commande=commande).order_by('created_at')
    #paginator = Paginator(agences, 25)  # Show 25  per page
    #page = request.GET.get('page')
    #agences = paginator.get_page(page)

    context = {
        'commande': commande,
        'historiques': historiques
    }
    return render(request, "commandes/commande_historique.html", context)

#Chauffeur: Choisir une commande
def assign_order_to_me(request):
    cmd_id = request.GET.get('id')
    commande = get_object_or_404(Commandes, id=cmd_id)
    commande.driver = request.user
    commande.save()
    data = {
        'statut': 'success',
        'message': 'Commande affectée'
    }
    return JsonResponse(data)


#Reclamations
def add_reclamation(request):
    form = ReclamationForm()
    # paginator = Paginator(agences, 25)  # Show 25  per page
    # page = request.GET.get('page')
    # agences = paginator.get_page(page)

    context = {
        'form': form,
    }
    return render(request, "commandes/ajout_reclamation.html", context)

from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, View
from django.contrib import messages
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Colis, Insurance, Commandes, HistoriqueCommandes, Reclamations, Tranche
from agences.models import Agences
from .forms import CommandesForm, InsuranceForm, ColisForm, CommandesFormset, Step1Form, Step2Form,ReclamationForm, ReclamationHandlerForm,TrancheForm
import random
import string

from zoom_transport.utils import render_to_pdf
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

@login_required
def mes_commandes(request):
    commandes = Commandes.objects.filter(colis__client=request.user)
    paginator = Paginator(commandes, 1)  # Show 25  per page
    page = request.GET.get('page')
    commandes = paginator.get_page(page)

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


def detail_commande(request):
    return

#Liste des commandes disponibles
def avalaible_orders(request):
    commandes = Commandes.objects.filter(driver__isnull=True, status=Commandes.ETAT_PAYE)
    context = {
        'commandes': commandes
    }
    return render(request, "commandes/commandes_disponibles.html", context)

def delivery_orders_by_driver(request):
    commandes = Commandes.objects.filter(driver=request.user).filter(Q(status=Commandes.ETAT_LIVRE) | Q(status=Commandes.ETAT_RECEPTIONNE))
    context = {
        'commandes': commandes
    }
    return render(request, "commandes/commandes_livres.html", context)

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


def historique_commande_admin(request,commande_id):
    commande = get_object_or_404(Commandes, id=commande_id)
    historiques = HistoriqueCommandes.objects.filter(commande=commande).order_by('created_at')
    #paginator = Paginator(agences, 25)  # Show 25  per page
    #page = request.GET.get('page')
    #agences = paginator.get_page(page)

    context = {
        'commande': commande,
        'historiques': historiques
    }
    return render(request, "commandes/commande_historique_admin.html", context)

#Chauffeur: Choisir une commande
@login_required
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
@login_required
def add_reclamation(request):
    reclamations = Reclamations.objects.filter(commande__colis__client=request.user)
    # paginator = Paginator(agences, 25)  # Show 25  per page
    # page = request.GET.get('page')
    # agences = paginator.get_page(page)
    if request.method == "POST":
        form = ReclamationForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Votre demande a été enregistrée')
            return redirect('commandes:add_reclamation')

        else:
            messages.error(request, 'Certaines données sont invalides')

    else:
        form = ReclamationForm(request.user)

    return render(request, "commandes/ajout_reclamation.html",  {
        'form': form,
        'reclamations': reclamations
    })
#Traitement reclamation

def add_handler_reclamation(request, commande_id):
    if request.method == "POST":
        form = ReclamationHandlerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre demande a été enregistrée')
        else:
            pass
    else:
        form = ReclamationHandlerForm()

    return render(request, "commandes/ajout_reclamation_handler.html",  {
        'form': form,
    })

def handler_reclamation_cmd(request, cmd_id):
    handler = ReclamationsHandler.objects.filter(reclamation__commande_id=cmd_id)
    data = serializers.serialize('json', handler)
    # if handler:
    #     data = {
    #         'statut': 'success',
    #         'data': data
    #     }
    print(cmd_id)
    return JsonResponse(data, safe=False)



#Administation 
def stats(request):
    return render(request, "default/stats.html", {})


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


def commande_view(request,commande_id):
    commande = get_object_or_404(Commandes, id=commande_id)
    #paginator = Paginator(agences, 25)  # Show 25  per page
    #page = request.GET.get('page')
    #agences = paginator.get_page(page)

    context = {
        'commande': commande
        }    
    return render(request, "commandes/commande_view.html", context)

def list_reclamation(request):
    reclamations = Reclamations.objects.all()
   
    context = {
            "reclamations": reclamations
    }
    return render (request, "commandes/liste_reclamations.html", context)


#Tranches

def tranche_create(request):
    tranches = Tranche.objects.filter().order_by('created_at')
    if request.method == "POST":
        form = TrancheForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Frais bien enregistrée')
            # return HttpResponseRedirect("/recipe/new/category")
            return redirect('commandes:tranche_create')
        else:
            pass
    else:
        form = TrancheForm()

    context = {
        'form': form,
        'object_list': tranches
        }

    return render(request, 'commandes/tranches_liste.html', context)


def tranche_update(request, tranche_id):
    tranche = Tranche.objects.get(id=tranche_id)
    tranches = Tranche.objects.filter().order_by('created_at')
    #paginator = Paginator(agences, 25)  # Show 25  per page
    #page = request.GET.get('page')
    #agences = paginator.get_page(page)
    if request.method == "POST":
        form = TrancheForm(request.POST, instance=tranche)
        if form.is_valid():
            form.save()
            messages.success(request, 'Frais mis à jour')
        return redirect('commandes:tranche_create')
    else:
        form = TrancheForm(instance=tranche)

    context = {
        'form': form,
        'object_list': tranches
    }
    return render(request, "commandes/tranches_liste.html", context)


def tranche_delete(request, tranche_id):
    tranche = get_object_or_404(Tranches, id=tranche_id)
    try:
        tranche.delete()
        messages.success(request, 'Tranche supprimée')

    except ProtectedError:
        messages.error(request, 'Suppression impossible')

    return redirect('commandes:tranche_create')


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
             'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
        pdf = render_to_pdf('commandes/invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
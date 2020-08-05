from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, View
from django.contrib import messages
from django.core import serializers
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.db.models import Q
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from .models import Colis, Insurance, Commandes, HistoriqueCommandes, Reclamations, Tranche, Package, Facture
from agences.models import Agences, Societe
from .forms import CommandesForm, InsuranceForm, ColisForm, CommandesFormset, Step1Form, Step2Form,ReclamationForm, ReclamationHandlerForm,TrancheForm, PackageForm
from .tables import CommandeTable, CommandeClientTable, CommandeDriverTable, ReclamationTable

from .filters import CommandesFilter
import random
import string
from weasyprint import HTML
from var_dump import var_dump





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
        if  commande.is_valid():
            self.object.save()

            commande.instance = self.object
            commande.save()

            messages.success(self.request, 'Commande enregistrée')

        else:
            messages.success(self.request, 'Certaines données sont invalides')

            #reference = random_string_generator()
            # qs_exists = Commandes.objects.filter(numero_commande=reference).exists()
            # if qs_exists:
            #     reference = random_string_generator()
        return super().form_valid(form)
    def get_success_url(self):

        return reverse("commandes:create_commande")


#Commande du client
@login_required
def mes_commandes(request):
    #Mes commandes en attente
    table = CommandeClientTable(Commandes.objects.filter(colis__client=request.user,status=Commandes.ETAT_PAYE))
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    #Commande livrés
    table2 = CommandeDriverTable(Commandes.objects.filter(colis__client=request.user).filter(Q(status=Commandes.ETAT_LIVRE) | Q(status=Commandes.ETAT_RECEPTIONNE)))
    table2.paginate(page=request.GET.get("page", 1), per_page=25)

    #Commande En cours
    table3 = CommandeDriverTable(Commandes.objects.filter(colis__client=request.user).filter(Q(status=Commandes.ETAT_EN_TRANSIT) | Q(status=Commandes.ETAT_EN_AGENCE)))
    table3.paginate(page=request.GET.get("page", 1), per_page=25)
 
    queryset = Commandes.objects.select_related().all()
    f = CommandesFilter(request.GET, queryset=queryset)

    context = {
        'table': table,
        'table2': table2,
        'table3': table3
    }
    return render(request, "commandes/mes_commandes.html", context)


def mes_commandes_detail(request,commande_ref):
    commande = get_object_or_404(Commandes, numero_commande=commande_ref)

    #paginator = Paginator(agences, 25)  # Show 25  per page
    #page = request.GET.get('page')
    #agences = paginator.get_page(page)

    context = {
        'commande': commande,

    }
    return render(request, "commandes/mes_commandes_detail.html", context)


def detail_commande(request):
    return

#Vue commande du chauffeur
def avalaible_orders(request):

    #Commande disponible
    table = CommandeDriverTable(Commandes.objects.filter(driver__isnull=True, status=Commandes.ETAT_PAYE))
    table.paginate(page=request.GET.get("page", 1), per_page=25)

    #Commande livrés
    table2 = CommandeDriverTable(Commandes.objects.filter(driver=request.user).filter(Q(status=Commandes.ETAT_LIVRE) | Q(status=Commandes.ETAT_RECEPTIONNE)))
    table2.paginate(page=request.GET.get("page", 1), per_page=25)

    #Commande En cours
    table3 = CommandeDriverTable(Commandes.objects.filter(driver=request.user).filter(Q(status=Commandes.ETAT_EN_TRANSIT) | Q(status=Commandes.ETAT_EN_AGENCE)))
    table3.paginate(page=request.GET.get("page", 1), per_page=25)


    queryset = Commandes.objects.select_related().all()
    f = CommandesFilter(request.GET, queryset=queryset)
    context = {
        'table': table,
        'table2': table2,
        'table3': table3
    }
    return render(request, "commandes/commandes_drivers.html", context)

def delivery_orders_by_driver(request):
    commandes = Commandes.objects.filter(driver=request.user).filter(Q(status=Commandes.ETAT_LIVRE) | Q(status=Commandes.ETAT_RECEPTIONNE))
    context = {
        'commandes': commandes
    }
    return render(request, "commandes/commandes_livres.html", context)

def etat_update(request):
    etat = request.GET.get('etat')
    cmd_id = request.GET.get('id')
    agence = None
    comment = ""
    commande = get_object_or_404(Commandes, id=cmd_id)
    #Si la commande est a l'etat payé on enregistre le montant et la commission

    commande.status = etat
    commande.agent = request.user 
    commande.save()
    if request.GET.get('agence'):
        agence = get_object_or_404(Agences, id=request.GET.get('agence'))
    if request.GET.get('comment'):
        comment = request.GET.get('comment')

    history = HistoriqueCommandes.objects.create(commande=commande, user=request.user, state=etat, agence=agence, comment=comment)
    

    data = {
        'statut': 'success',
        'message': 'La commande a été mise à jour'
    }
    return JsonResponse(data)

def historique_commande(request,commande_ref):
    commande = get_object_or_404(Commandes, numero_commande = commande_ref)
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
    cmd_num = request.GET.get('id')
    commande = get_object_or_404(Commandes, numero_commande=cmd_num)
    if commande.accepted == Commandes.ETAT_NON_ACCEPTE:
        commande.accepted = Commandes.ETAT_ACCEPTE
        commande.driver = request.user

    else:
        commande.accepted = Commandes.ETAT_NON_ACCEPTE
        commande.driver = None

    commande.save()
    data = {
        'statut': 'success',
        'message': 'Commande affectée'
    }
    return JsonResponse(data)


@login_required
def commande_view_driver(request,commande_ref):
    commande = get_object_or_404(Commandes, numero_commande=commande_ref)
    context = {
        'commande': commande
        }    
    return render(request, "commandes/detail.html", context)


# def mes_commissions(request):
    
#     return render ''


#Enregistrer une Reclamations
@login_required
def add_reclamation(request):
    reclamations = Reclamations.objects.filter(commande__colis__client=request.user)
    paginator = Paginator(reclamations, 25)  # Show 25  per page
    page = request.GET.get('page')
    reclamations = paginator.get_page(page)
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

#Traitement d'une reclamation
@login_required
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


@login_required
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
@login_required
def stats(request):
    return render(request, "default/stats.html", {})

@login_required
class FilteredCommandesListView(SingleTableMixin, FilterView):
    table_class = CommandeTable
    model = Commandes

    template_name = 'commandes/commandes_liste.html'
    paginate_by = 2
    ordering = ['date_depot']

    filterset_class = CommandesFilter



def commandes_liste(request):
    table = CommandeTable(Commandes.objects.filter().order_by('date_depot'))
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    queryset = Commandes.objects.select_related().all()
    f = CommandesFilter(request.GET, queryset=queryset)

    form_step1 = Step1Form
    form_step2 = Step2Form
    #paginator = Paginator(agences, 25)  # Show 25  per page
    #page = request.GET.get('page')
    #agences = paginator.get_page(page)

    context = {
        'table': table,
        'filter': f,
        'form_step1': form_step1,
        'form_step2': form_step2
    }
    return render(request, "commandes/commandes_liste.html", context)

@login_required
def commande_view(request,commande_id):
    commande = get_object_or_404(Commandes, id=commande_id)
    context = {
        'commande': commande
        }    
    return render(request, "commandes/commande_view.html", context)




@login_required
def list_reclamation(request):
    table = ReclamationTable(Reclamations.objects.all())
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    context = {
            "table": table
    }
    return render (request, "commandes/liste_reclamations.html", context)



#PaKAGE Envoi
@login_required
def package_create(request):
    packages = Package.objects.filter().order_by('created_at')
    paginator = Paginator(packages, 25)  # Show 25  per page
    page = request.GET.get('page')
    packages = paginator.get_page(page)
    if request.method == "POST":
        form = PackageForm()

        if form.is_valid():
            form.save()
            messages.success(request, 'Package enregistré')
            return redirect('commandes:package_create')

        else:
            messages.error(request, 'Certaines données sont invalides')

    else:
        form = PackageForm()

    return render(request, "commandes/ajout_package.html",  {
        'form': form,
        'packages': packages
    })

@login_required
def package_update(request, package_id):
    package = Package.objects.get(id=package_id)
    packages = Package.objects.filter().order_by('created_at')
    #paginator = Paginator(agences, 25)  # Show 25  per page
    #page = request.GET.get('page')
    #agences = paginator.get_page(page)
    if request.method == "POST":
        form = PackageForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, 'Package mis à jour')
        return redirect('commandes:package_create')
    else:
        form = PackageForm(instance=package)

    context = {
        'form': form,
        'packages': packages
    }
    return render(request, "commandes/ajout_package.html", context)


@login_required
def package_delete(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    try:
        package.delete()
        messages.success(request, 'Package supprimée')

    except ProtectedError:
        messages.error(request, 'Suppression impossible')

    return redirect('commandes:package_create')

#Tranches
@login_required
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

@login_required
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

@login_required
def tranche_delete(request, tranche_id):
    tranche = get_object_or_404(Tranche, id=tranche_id)
    try:
        tranche.delete()
        messages.success(request, 'Tranche supprimée')

    except ProtectedError:
        messages.error(request, 'Suppression impossible')

    return redirect('commandes:tranche_create')




class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        commande = get_object_or_404(Commandes, numero_commande=self.kwargs['commande_ref'])
        societe = get_object_or_404(Societe, id=1)
        data = getTrancheData(commande)

        pdf = render_to_pdf('commandes/invoice.html', {"commande":commande, 'data':data, 'societe':societe})
        return HttpResponse(pdf, content_type='application/pdf')


def generate(request, commande_ref):
    commande = get_object_or_404(Commandes, numero_commande=commande_ref)
    try:
        facture = Facture.objects.get(commande = commande)
    except Facture.DoesNotExist:
        facture = Facture.objects.create(commande=commande, status="Payé")

    societe = get_object_or_404(Societe, id=1)

    filename = 'facture_'+commande_ref+'.pdf'
    html_string = render_to_string('commandes/facture.html', {'facture': facture, 'societe':societe})
    
    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/'+filename);

    fs = FileSystemStorage('/tmp')
    with fs.open(filename) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response
    return response 



def getTrancheData(colis):
    tranches = Tranche.objects.all()
    data = {
            "amount": 0,
            "commission": 0
        }
    for t in tranches:
        minimum = colis.weight
        if colis.weight >= t.min_weight and colis.weight  <= t.max_weight:
            data = {
                "amount": t.price,
                "commission":  t.commission
            }
        return data
    return data
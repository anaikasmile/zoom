from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages

from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.views.generic import ListView, CreateView
from .forms import AgenceForm, TypeVehiculeForm, VehiculesForm
from .models import Agences, TypeVehicules, Vehicules
from affection.models import AgenceUser
from django.db.models import ProtectedError
from .tables import AgenceTable, VehiculeTable
from datatableview.views import DatatableView, Datatable
from django.template.defaultfilters import timesince


# Create your views here.
def agence_create(request):
    table = AgenceTable(Agences.objects.filter().order_by('name'))
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    if request.method == "POST":
        form = AgenceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agence bien enregistrée')
            return redirect('agences:agence-create')
        else:
            pass
    else:
        form = AgenceForm()
    context = {
        'form': form,
        'table': table

    }
    return render(request, 'agences/agences_list.html', context)

def agence_update(request, agence_id):
    agence = Agences.objects.get(id=agence_id)
    table = AgenceTable(Agences.objects.filter().order_by('name'))
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    if request.method == "POST":
        form = AgenceForm(request.POST, request.FILES, instance=agence)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agence mise à jour')
        return redirect('agences:agence-create')
    else:
        form = AgenceForm(instance=agence)

    context = {
        'form': form,
        'table': table
    }
    return render(request, "agences/agences_list.html", context)


def agence_view(request, agence_id):

    agence = Agences.objects.get(id=agence_id)
    #liste des agents par agences.
    agents = AgenceUser.objects.filter(agence=agence).order_by('agent__last_name')

    context = {
        'agence': agence,
        'agents': agents
    }
    return render(request, "agences/agences_view.html", context)


def agence_delete(request, agence_id):
    agence = get_object_or_404(Agences, id=agence_id)
    try:
        agence.delete()
        messages.success(request, 'Agence supprimée')

    except ProtectedError:
        messages.error(request, 'Suppression impossible')

    return redirect('agences:agence-create')


#Vehicules
def vehicule_create(request):
    vehicules = Vehicules.objects.filter().order_by('-created_at')
    paginator = Paginator(vehicules, 25)  # Show 25  per page
    page = request.GET.get('page')
    vehicules = paginator.get_page(page)
    if request.method == "POST":
        form = VehiculesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Véhicule enregistrée')
            # return HttpResponseRedirect("/recipe/new/category")
            return redirect('agences:vehicule-create')

        else:
            pass
    else:
        form = VehiculesForm()
    context = {
        'form': form,
        'object_list': vehicules

    }
    return render(request, 'agences/vehicules_create.html', context)


# class VehiculeTable(Datatable):
#     class Meta:

#         columns = [
#                 'id',
#                 'immatriculation',
#                 'type',
#                 'marque',
#                 'modele',
#                 'nb_place',
#                 'etat',
#                 'user',
#                 ]
#         ordering = ['-created_at']

#         hidden_columns = [ "id"]
#         search_fields = ["immatriculation", "type", "marque", "user"]

        

            
def vehicule_list(request):           
    table = VehiculeTable(Vehicules.objects.filter().order_by('-created_at'))
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    context = {
        'table': table
    }
    return render(request, 'agences/vehicules_list.html', context)

   

def vehicule_update(request, vehicule_id):
    vehicule = Vehicules.objects.get(id=vehicule_id)
    vehicules = Vehicules.objects.filter().order_by('-created_at')
    paginator = Paginator(vehicules, 25)  # Show 25  per page
    page = request.GET.get('page')
    vehicules = paginator.get_page(page)
    if request.method == "POST":
        form = VehiculesForm(request.POST, request.FILES, instance=vehicule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Véhicule mis à jour')
        return redirect('agences:vehicule-create')
    else:
        form = VehiculesForm(instance=vehicule)

    context = {
        'form': form,
        'object_list': vehicules
    }
    return render(request, "agences/vehicules_create.html", context)

def vehicule_detail(request, vehicule_id):
    vehicule = Vehicules.objects.get(id=vehicule_id)
    #paginator = Paginator(agences, 25)  # Show 25  per page
    #page = request.GET.get('page')
    #agences = paginator.get_page(page)

    context = {
        'vehicule': vehicule,
    }
    return render(request, "agences/vehicules_detail.html", context)



def vehicule_delete(request, vehicule_id):
    vehicule = get_object_or_404(Vehicules, id=vehicule_id)
    try:
        vehicule.delete()
        messages.success(request, 'Véhicule supprimée')
    except ProtectedError:
        messages.error(request, 'Suppression impossible')
    return redirect('agences:vehicule-create')

def type_vehicule_create(request):
    type_vehicules = TypeVehicules.objects.filter().order_by('-created_at')
    type_vehicules = TypeVehicules.objects.filter().order_by('-created_at')
    paginator = Paginator(type_vehicules, 25)  # Show 25  per page
    page = request.GET.get('page')
    type_vehicules = paginator.get_page(page)
    if request.method == "POST":
        form = TypeVehiculeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Type enregistré')
            return redirect('agences:type-vehicule-create')
        else:
            pass
    else:
        form = TypeVehiculeForm()
    context = {
        'form': form,
        'object_list': type_vehicules

    }
    return render(request, 'agences/type_vehicules_list.html', context)

def type_vehicule_update(request, type_vehicule_id):
    type_vehicule = TypeVehicules.objects.get(id=type_vehicule_id)
    type_vehicules = TypeVehicules.objects.filter().order_by('-created_at')
    paginator = Paginator(type_vehicules, 25)  # Show 25  per page
    page = request.GET.get('page')
    type_vehicules = paginator.get_page(page)
    if request.method == "POST":
        form = TypeVehiculeForm(request.POST, request.FILES, instance=type_vehicule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Type mis à jour')
        return redirect('agences:type-vehicule-create')
    else:
        form = TypeVehiculeForm(instance=type_vehicule)

    context = {
        'form': form,
        'object_list': type_vehicules
    }
    return render(request, "agences/type_vehicules_list.html", context)

def type_vehicule_delete(request, type_vehicule_id):
    type_vehicule = get_object_or_404(TypeVehicules, id=type_vehicule_id)
    try:
        type_vehicule.delete()
        messages.success(request, 'Type supprimé')
    except ProtectedError:
        messages.error(request, 'Suppression impossible')
    return redirect('agences:type-vehicule-create')
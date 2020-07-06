from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages

from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.views.generic import ListView, CreateView
from .forms import AgenceForm, TypeVehiculeForm, VehiculesForm
from .models import Agences, TypeVehicules, Vehicules
# Create your views here.
def agence_create(request):
    agences = Agences.objects.filter().order_by('-created_at')
    if request.method == "POST":
        form = AgenceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agence bien enregistrée')
            # return HttpResponseRedirect("/recipe/new/category")
            return redirect('agences:agence-create')
        else:
            pass
    else:
        form = AgenceForm()
    context = {
        'form': form,
        'object_list': agences

    }
    return render(request, 'agences/agences_list.html', context)

def agence_update(request, agence_id):

    agence = Agences.objects.get(id=agence_id)
    agences = Agences.objects.filter().order_by('-created_at')
    #paginator = Paginator(agences, 25)  # Show 25  per page
    #page = request.GET.get('page')
    #agences = paginator.get_page(page)
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
        'object_list': agences
    }
    return render(request, "agences/agences_list.html", context)


def agence_delete(request, agence_id):
    agence = get_object_or_404(Agences, id=agence_id)
    agence.delete()
    messages.success(request, 'Agence supprimée')
    return redirect('agences:agence-create')


#Vehicules
def vehicule_create(request):
    vehicules = Vehicules.objects.filter().order_by('-created_at')
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
    return render(request, 'agences/vehicules_list.html', context)

def vehicule_update(request, vehicule_id):
    vehicule = Vehicules.objects.get(id=vehicule_id)
    vehicules = Vehicules.objects.filter().order_by('-created_at')
    #paginator = Paginator(agences, 25)  # Show 25  per page
    #page = request.GET.get('page')
    #agences = paginator.get_page(page)
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
    return render(request, "agences/vehicules_list.html", context)

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
    vehicule.delete()
    messages.success(request, 'Véhicule supprimée')
    return redirect('agences:vehicule-create')

def type_vehicule_create(request):
    type_vehicules = TypeVehicules.objects.filter().order_by('-created_at')
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
    #paginator = Paginator(agences, 25)  # Show 25  per page
    #page = request.GET.get('page')
    #agences = paginator.get_page(page)
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
    type_vehicule.delete()
    messages.success(request, 'Type supprimé')
    return redirect('agences:type-vehicule-create')
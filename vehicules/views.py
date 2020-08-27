from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages

from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.views.generic import ListView, CreateView
from .models import Vehicules, TypeVehicules
from utilisateurs.models import User

from .forms import VehiculesForm, TypeVehiculeForm
from django.contrib.auth.decorators import login_required
from .tables import VehiculeTable


# Create your views here.
#Vehicules
@login_required
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
            return redirect('vehicules:vehicule-create')

        else:
            pass
    else:
        form = VehiculesForm()
    context = {
        'form': form,
        'object_list': vehicules

    }
    return render(request, 'vehicules/vehicules_create.html', context)


@login_required
def vehicule_list(request):           
    table = VehiculeTable(Vehicules.objects.filter().order_by('-created_at'))
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    context = {
        'table': table
    }
    return render(request, 'vehicules/vehicules_list.html', context)

   
@login_required
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
        return redirect('vehicules:vehicule-create')
    else:
        form = VehiculesForm(instance=vehicule)

    context = {
        'form': form,
        'object_list': vehicules
    }
    return render(request, "vehicules/vehicules_create.html", context)

@login_required
def vehicule_detail(request, vehicule_id):
    vehicule = Vehicules.objects.get(id=vehicule_id)
    context = {
        'vehicule': vehicule,
    }
    return render(request, "vehicules/vehicules_detail.html", context)


@login_required
def vehicule_delete(request, vehicule_id):
    vehicule = get_object_or_404(Vehicules, id=vehicule_id)
    try:
        vehicule.delete()
        messages.success(request, 'Véhicule supprimée')
    except ProtectedError:
        messages.error(request, 'Suppression impossible')
    return redirect('vehicules:vehicule-create')

@login_required
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
            return redirect('vehicules:type-vehicule-create')
        else:
            pass
    else:
        form = TypeVehiculeForm()
    context = {
        'form': form,
        'object_list': type_vehicules

    }
    return render(request, 'vehicules/type_vehicules_list.html', context)

@login_required
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
        return redirect('vehicules:type-vehicule-create')
    else:
        form = TypeVehiculeForm(instance=type_vehicule)

    context = {
        'form': form,
        'object_list': type_vehicules
    }
    return render(request, "vehicules/type_vehicules_list.html", context)

@login_required
def type_vehicule_delete(request, type_vehicule_id):
    type_vehicule = get_object_or_404(TypeVehicules, id=type_vehicule_id)
    try:
        type_vehicule.delete()
        messages.success(request, 'Type supprimé')
    except ProtectedError:
        messages.error(request, 'Suppression impossible')
    return redirect('vehicules:type-vehicule-create')
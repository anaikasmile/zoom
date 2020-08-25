from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse

from .models import City, District
from .forms import CityForm, DistrictForm
from django.views.generic.edit import FormView, CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import ProtectedError

from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.

# City views
def city_create(request):
    cities = City.objects.filter().order_by('name')
    paginator = Paginator(cities, 25)  # Show 25  per page
    page = request.GET.get('page')
    cities = paginator.get_page(page)
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ville enregistrée')
        else:
            messages.error(request, 'Echec  enregistrement')

        return redirect('geolocalisation:city_create')
    else:
        form = CityForm()
    context = {
        'form': form,
        'object_list': cities
    }
    return render(request, 'geolocalisation/city_list.html', context)

def city_update(request, city_id):

    city = City.objects.get(id=city_id)
    cities = City.objects.filter().order_by('name')
    paginator = Paginator(cities, 25)  # Show 25  per page
    page = request.GET.get('page')
    cities = paginator.get_page(page)
    if request.method == "POST":
        form = CityForm(request.POST, request.FILES, instance=city)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ville mise à jour')
        return redirect('geolocalisation:city_create')
    else:
        form = CityForm(instance=city)

    context = {
        'form': form,
        'object_list': cities
    }
    return render(request, "geolocalisation/city_list.html", context)


def city_delete(request, city_id):
    city = get_object_or_404(City, id=city_id)
    try:
        city.delete()
        messages.success(request, 'Ville supprimée')
    except ProtectedError:
        messages.error(request, 'Suppression impossible!')
    return redirect('geolocalisation:city_create')

# District views
# Create your views here.
def district_create(request):
    district = District.objects.filter().order_by('name')
    paginator = Paginator(district, 25)  # Show 25  per page
    page = request.GET.get('page')
    district = paginator.get_page(page)
    if request.method == "POST":
        form = DistrictForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quartier enregistré')
            return redirect('geolocalisation:district_create')
        else:
            pass
    else:
        form = DistrictForm()
    context = {
        'form': form,
        'object_list': district
    }
    return render(request, 'geolocalisation/district_list.html', context)

def district_update(request, district_id):

    district = District.objects.get(id=district_id)
    districts = District.objects.filter().order_by('name')
    paginator = Paginator(districts, 25)  # Show 25  per page
    page = request.GET.get('page')
    districts = paginator.get_page(page)
    if request.method == "POST":
        form = DistrictForm(request.POST, request.FILES, instance=district)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quartier mis à jour')
        return redirect('geolocalisation:district_create')
    else:
        form = DistrictForm(instance=district)

    context = {
        'form': form,
        'object_list': districts
    }
    return render(request, "geolocalisation/district_list.html", context)


def district_delete(request, district_id):
    district = get_object_or_404(District, id=district_id)
    try:
        district.delete()
        messages.success(request, 'Quartier supprimée')

    except ProtectedError:
        messages.error(request, 'Suppression impossible!')

    return redirect('geolocalisation:district_create')



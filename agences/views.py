from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages

from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.views.generic import ListView, CreateView
from .forms import AgenceForm
from .models import Agences
from affection.models import AgenceUser
from django.db.models import ProtectedError
from .tables import AgenceTable #VehiculeTable
from datatableview.views import DatatableView, Datatable
from django.template.defaultfilters import timesince
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.
@login_required
@staff_member_required
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

@login_required
@staff_member_required
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

@login_required
@staff_member_required
def agence_view(request, agence_id):

    agence = Agences.objects.get(id=agence_id)
    #liste des agents par agences.
    agents = AgenceUser.objects.filter(agence=agence).order_by('agent__last_name')

    context = {
        'agence': agence,
        'agents': agents
    }
    return render(request, "agences/agences_view.html", context)

@login_required
@staff_member_required
def agence_delete(request, agence_id):
    agence = get_object_or_404(Agences, id=agence_id)
    try:
        agence.delete()
        messages.success(request, 'Agence supprimée')

    except ProtectedError:
        messages.error(request, 'Suppression impossible')

    return redirect('agences:agence-create')



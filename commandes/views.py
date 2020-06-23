from django.shortcuts import render, reverse
from .models import Colis, Insurance, Commandes
from .forms import CommandesForm, InsuranceForm, ColisForm, CommandesFormset
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
            commande.save(commit=False)
            reference = random_string_generator()
            # qs_exists = Commandes.objects.filter(numero_commande=reference).exists()
            # if qs_exists:
            #     reference = random_string_generator()
            commande.save()
        return super().form_valid(form)
    def get_success_url(self):
        messages.success(self.request, 'Commande enregistrée')
        return reverse("commandes:create_commande")
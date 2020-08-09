from django.contrib import admin
from .models import Agences, TypeVehicules, Vehicules, Societe
# Register your models here.
admin.site.register(Agences)
admin.site.register(Vehicules)
admin.site.register(TypeVehicules)
admin.site.register(Societe)

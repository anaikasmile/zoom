from django.contrib import admin
from .models import Colis, Insurance, Commandes, HistoriqueCommandes
# Register your models here.
admin.site.register(Colis)
admin.site.register(Insurance)
admin.site.register(Commandes)
admin.site.register(HistoriqueCommandes)

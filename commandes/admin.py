from django.contrib import admin
from .models import Colis, Insurance, Commandes, HistoriqueCommandes, Reclamations, ReclamationsHandler, Tranche, Package, Facture
# Register your models here.
admin.site.register(Colis)
admin.site.register(Insurance)
admin.site.register(Commandes)
admin.site.register(HistoriqueCommandes)
admin.site.register(Reclamations)
admin.site.register(ReclamationsHandler)
admin.site.register(Tranche)
admin.site.register(Package)
admin.site.register(Facture)

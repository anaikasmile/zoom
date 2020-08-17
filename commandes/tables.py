import django_tables2 as tables
import itertools

from django_tables2 import TemplateColumn, LinkColumn
from .models import Commandes, Reclamations
from django_tables2.utils import A  # alias for Accessor


class CommandeTable(tables.Table):
    client  = tables.LinkColumn("utilisateurs:user_profile", text=lambda record: record.colis.client, args=[A("colis__client__id")]) 
    driver  = tables.LinkColumn("utilisateurs:user_profile", text=lambda record: record.driver, args=[A("driver__id")]) 
    etat = tables.Column(accessor="getEtatLibelle")
    date_depot = tables.DateTimeColumn(format ='d/m/Y')
    numero_commande = tables.LinkColumn("commandes:commande_view", args=[A("id")])

    actions  = TemplateColumn(template_name="commandes/includes/commande_actions.html", attrs={"td": {"class": "text-right"}})
    class Meta:
        model = Commandes
        sequence = ('id','date_depot','numero_commande','price','commission','client','etat','driver','actions')

        exclude = {'colis','accepted','status','observation','insurance','updated_at', 'date_reception', 'city_depart', 'city_arrive', 'created_at', 'package','agent'}
        template_name = "django_tables2/bootstrap.html"
       	attrs = {
	        "th" : {
	            "_ordering": {
	                "orderable": "sortable", # Instead of `orderable`
	                "ascending": "ascend",   # Instead of `asc`
	                "descending": "descend"  # Instead of `desc`
	            }
        	}
    	}

 
class CommandeClientTable(tables.Table):
    etat = tables.Column(accessor="getEtatLibelle")
    ID  = tables.Column(empty_values=())
    date_depot = tables.DateTimeColumn(format ='d/m/Y')
    date_reception = tables.DateTimeColumn(format ='d/m/Y')

    actions  = TemplateColumn(template_name="commandes/includes/commande_client_actions.html", attrs={"td": {"class": "text-right"}})

    class Meta:
        model = Commandes
        sequence = ('ID', 'numero_commande','colis','date_depot','price','etat','actions')
        exclude = {'status', 'accepted','id','commission','observation','insurance','updated_at', 'date_reception', 'city_depart', 'city_arrive', 'created_at', 'package','agent','driver'}
        template_name = "django_tables2/bootstrap.html"
        attrs = {
	        "th" : {
	            "_ordering": {
	                "orderable": "sortable", # Instead of `orderable`
	                "ascending": "ascend",   # Instead of `asc`
	                "descending": "descend"  # Instead of `desc`
	            }
        	}
    	}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_ID(self):
        return "%d" % next(self.counter)


class CommandeDriverTable(tables.Table):
    etat = tables.Column(accessor="getEtatLibelle")
    ID  = tables.Column(empty_values=())
    date_depot = tables.DateTimeColumn(format ='d/m/Y')
    date_reception = tables.DateTimeColumn(format ='d/m/Y')


    actions  = TemplateColumn(template_name="commandes/includes/commande_driver_actions.html", attrs={"td": {"class": "text-right"}})

    class Meta:
        model = Commandes
        sequence = ('ID', 'numero_commande','colis','city_depart', 'city_arrive','date_depot','date_reception','commission','etat','actions')
        exclude = {'status', 'id','observation','insurance','updated_at','created_at',  'price', 'package','agent','driver','accepted'}
        template_name = "django_tables2/bootstrap.html"
        attrs = {
	        "th" : {
	            "_ordering": {
	                "orderable": "sortable", # Instead of `orderable`
	                "ascending": "ascend",   # Instead of `asc`
	                "descending": "descend"  # Instead of `desc`
	            }
        	}
    	}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_ID(self):
        return "%d" % next(self.counter)


class ReclamationTable(tables.Table):
    etat = TemplateColumn(template_name="commandes/includes/reclamation_traitement.html", attrs={"td": {"class": ""}})
    actions  = TemplateColumn(template_name="commandes/includes/reclamation_actions.html", attrs={"td": {"class": ""}})
    created_at = tables.DateTimeColumn(format ='d/m/Y')

    commande  = tables.LinkColumn("commandes:commande_view", text=lambda record: record.commande, args=[A("commande__id")]) 

    class Meta:
        model = Reclamations
        sequence = ('id', 'created_at', 'commande','type', 'observation','image','etat','actions')
        exclude = ['updated_at']
        template_name = "django_tables2/bootstrap.html"
       	attrs = {
	        "th" : {
	            "_ordering": {
	                "orderable": "sortable", # Instead of `orderable`
	                "ascending": "ascend",   # Instead of `asc`
	                "descending": "descend"  # Instead of `desc`
	            }
        	}
    	}
        def render_etat(self, value, record):
            return format_html("<b>{} {}</b>", value, record.reclamationHandler.all)

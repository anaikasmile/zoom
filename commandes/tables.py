import django_tables2 as tables
import itertools

from django_tables2 import TemplateColumn
from .models import Commandes


class CommandeTable(tables.Table):
    client  = tables.Column(accessor="colis__client")
    etat = tables.Column(accessor="getEtatLibelle")
    actions  = TemplateColumn(template_name="commandes/includes/commande_actions.html", attrs={"td": {"class": "text-right"}})
    class Meta:
        model = Commandes
        exclude = {'status','observation','insurance','updated_at', 'date_reception', 'city_depart', 'city_arrive', 'created_at', 'package','agent'}
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
    actions  = TemplateColumn(template_name="commandes/includes/commande_client_actions.html", attrs={"td": {"class": "text-right"}})

    class Meta:
        model = Commandes
        sequence = ('ID', 'numero_commande','colis','date_depot','price','etat','actions')
        exclude = {'status', 'id','commission','observation','insurance','updated_at', 'date_reception', 'city_depart', 'city_arrive', 'created_at', 'package','agent','driver'}
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
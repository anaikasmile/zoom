import django_tables2 as tables
from django_tables2 import TemplateColumn
from .models import Agences
from django_tables2.utils import A  # alias for Accessor


class AgenceTable(tables.Table):
    actions  = TemplateColumn(template_name="agences/includes/agences_actions.html", attrs={"td": {"class": ""}})
    class Meta:
        model = Agences
        exclude = {'addresses','updated_at', 'created_at'}
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

   

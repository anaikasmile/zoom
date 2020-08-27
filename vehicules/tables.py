import django_tables2 as tables
from django_tables2 import TemplateColumn
from .models import Vehicules
from django_tables2.utils import A  # alias for Accessor


class VehiculeTable(tables.Table):
    actions  = TemplateColumn(template_name="vehicules/vehicules_actions.html", attrs={"td": {"class": ""}})
    user  = tables.LinkColumn("utilisateurs:user_profile", text=lambda record: record.user, args=[A("user__id")]) 

    class Meta:
        model = Vehicules
        template_name = "django_tables2/bootstrap.html"
        exclude = {'updated_at', 'created_at','description','etat'}

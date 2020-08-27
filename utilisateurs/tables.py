import django_tables2 as tables
from django_tables2 import TemplateColumn
from .models import User, Person


class UserTable(tables.Table):
    sexe  = tables.Column(accessor="sexe")
    tel  = tables.Column(accessor="tel__as_e164")
    date_joined = tables.DateTimeColumn(format ='d/m/Y')
    agence = tables.Column(accessor="agent__agence")
    #agence  = TemplateColumn(template_name="utilisateurs/includes/users_agences.html", attrs={"td": {"class": ""}})

    actions  = TemplateColumn(template_name="utilisateurs/includes/users_actions.html", attrs={"td": {"class": ""}})
    class Meta:
        model = User
        sequence = ('id', 'last_name','first_name', 'sexe', 'email','tel','agence')
        exclude = {'photo','adresse','username','password', 'last_login', 'birth_date', 'is_staff', 'is_superuser', 'is_active', 'date_joined'}
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


class DriverTable(tables.Table):
    sexe  = tables.Column(accessor="sexe")
    tel  = tables.Column(accessor="tel__as_e164")
    date_joined = tables.DateTimeColumn(format ='d/m/Y')
    #agence = tables.Column(accessor="")
    #agence  = TemplateColumn(template_name="utilisateurs/includes/users_agences.html", attrs={"td": {"class": ""}})

    actions  = TemplateColumn(template_name="utilisateurs/includes/users_actions.html", attrs={"td": {"class": ""}})
    class Meta:
        model = User
        sequence = ('id', 'last_name','first_name', 'sexe', 'email','tel')
        exclude = {'photo','adresse','username','password', 'last_login', 'is_staff', 'is_superuser', 'is_active', 'date_joined'}
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

class ClientTable(tables.Table):
    sexe  = tables.Column(accessor="sexe")
    tel  = tables.Column(accessor="tel__as_e164")
    date_joined = tables.DateTimeColumn(format ='d/m/Y')
    actions  = TemplateColumn(template_name="utilisateurs/includes/users_actions.html", attrs={"td": {"class": "text-right"}})
    class Meta:
        model = User
        sequence = ('id', 'last_name','first_name', 'sexe', 'email','tel')
        exclude = {'username','birth_date', 'password', 'last_login', 'is_staff', 'is_superuser', 'is_active', 'adresse','photo'}
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

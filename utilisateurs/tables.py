import django_tables2 as tables
from django_tables2 import TemplateColumn
from .models import User, Person


class UserTable(tables.Table):
    sexe  = tables.Column(accessor="user.person_sexe")
    tel  = tables.Column(accessor="user.person_tel")


    actions  = TemplateColumn(template_name="utilisateurs/includes/users_actions.html", attrs={"td": {"class": "text-right"}})
    class Meta:
        model = User
        exclude = {'password', 'last_login', 'is_staff', 'is_superuser', 'is_active'}
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
    nom  = tables.Column(accessor="person.user.last_name")
    prenom  = tables.Column(accessor="person.user.first_name")
    birth_date = tables.DateTimeColumn(format ='d/m/Y')


    actions  = TemplateColumn(template_name="utilisateurs/includes/users_actions.html", attrs={"td": {"class": "text-right"}})
    class Meta:
        model = Person
        sequence = ('id', 'nom', 'prenom','sexe', 'tel','birth_date','job','actions')

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

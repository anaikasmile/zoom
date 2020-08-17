import django_tables2 as tables
from django_tables2 import TemplateColumn
from .models import User, Person


class UserTable(tables.Table):
    sexe  = tables.Column(accessor="person__sexe")
    tel  = tables.Column(accessor="person__tel__as_e164")
    date_joined = tables.DateTimeColumn(format ='d/m/Y')
    #agence = tables.Column(accessor="")

    actions  = TemplateColumn(template_name="utilisateurs/includes/users_actions.html", attrs={"td": {"class": "text-right"}})
    class Meta:
        model = User
        sequence = ('id', 'last_name','first_name', 'sexe', 'email','tel')
        exclude = {'username','password', 'last_login', 'is_staff', 'is_superuser', 'is_active','user_type', 'date_joined'}
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
    sexe  = tables.Column(accessor="person__sexe")
    tel  = tables.Column(accessor="person__tel")
    date_joined = tables.DateTimeColumn(format ='d/m/Y')
    actions  = TemplateColumn(template_name="utilisateurs/includes/users_actions.html", attrs={"td": {"class": "text-right"}})
    class Meta:
        model = User
        sequence = ('id', 'last_name','first_name', 'sexe', 'email','tel')
        exclude = {'username','password', 'last_login', 'is_staff', 'is_superuser', 'is_active','user_type'}
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

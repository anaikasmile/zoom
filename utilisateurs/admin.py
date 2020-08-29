from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Person, Agent
# Register your models here.

UserAdmin.fieldsets += ('Custom fields set', {'fields': ('tel', 'sexe')}),

class PersonInline(admin.StackedInline):
    model = Person
    can_delete = False
    verbose_name_plural = 'Person'
    fk_name = 'user'

# class CustomUserAdmin(UserAdmin):
#     inlines = (PersonInline, )

#     def get_inline_instances(self, request, obj=None):
#         if not obj:
#             return list()
#         return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.register(User)
admin.site.register(Person)
admin.site.register(Agent)
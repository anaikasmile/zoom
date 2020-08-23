from django.db import models
from utilisateurs.models import User
from agences.models import Agences

# Create your models here.
class AgenceUser(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="affectation_agent")
    agence = models.ForeignKey(Agences, on_delete=models.CASCADE, related_name="affectation_agence")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Modifié le")
    def __str__(self):
        return self.agence.name 
    class Meta:
        """docstring for Meta"""
        constraints = [
                models.UniqueConstraint(fields=['agent', 'agence'], name='affectation')
            ]
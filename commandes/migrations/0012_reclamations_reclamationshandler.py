# Generated by Django 2.2.13 on 2020-07-07 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('commandes', '0011_commandes_driver'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reclamations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('type', models.CharField(blank=True, choices=[('Endommagé', 'Endommagé'), ('Perdu', 'Perdu'), ('Délai dépassé', 'Délai dépassé')], max_length=50, null=True, verbose_name='Type d incident')),
                ('observation', models.TextField(blank=True, verbose_name='Observations')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commandeIncident', to='commandes.Commandes')),
            ],
        ),
        migrations.CreateModel(
            name='ReclamationsHandler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('type', models.CharField(blank=True, choices=[('En cours de traitement', 'En cours de traitement'), ('Résolu', 'Résolu'), ('Non résolu', 'Non résolu')], max_length=50, null=True, verbose_name='Type d incident')),
                ('commentaire', models.TextField(blank=True, verbose_name='Commentaire')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userReclamations', to=settings.AUTH_USER_MODEL)),
                ('reclamation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reclamationHandler', to='commandes.Reclamations')),
            ],
        ),
    ]
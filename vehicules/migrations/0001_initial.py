# Generated by Django 2.2.13 on 2020-08-26 20:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeVehicules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=200, verbose_name='Type')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marque', models.CharField(blank=True, max_length=200, null=True, verbose_name='Marque')),
                ('modele', models.CharField(blank=True, max_length=200, null=True, verbose_name='Modèle')),
                ('immatriculation', models.CharField(blank=True, max_length=200, null=True, verbose_name='immatriculation *')),
                ('nb_place', models.IntegerField(blank=True, null=True, verbose_name='Nb places')),
                ('etat', models.TextField(blank=True, null=True, verbose_name='Etat')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vehicules.TypeVehicules', verbose_name='Type *')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vehicules', to=settings.AUTH_USER_MODEL, verbose_name='Chauffeur')),
            ],
        ),
    ]
# Generated by Django 2.2.13 on 2020-08-01 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('commandes', '0018_auto_20200728_2018'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='tranche',
            name='tranche_unique',
        ),
        migrations.AddField(
            model_name='commandes',
            name='agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commandes_agent', to=settings.AUTH_USER_MODEL, verbose_name='Agent'),
        ),
        migrations.AlterField(
            model_name='colis',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Créé le'),
        ),
        migrations.AlterField(
            model_name='colis',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Modifié le'),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='city_arrive',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cityArrival', to='geolocalisation.City', verbose_name="Ville d'arrivée"),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='city_depart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cityDepart', to='geolocalisation.City', verbose_name='Ville de départ'),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='colis',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='colis', to='commandes.Colis', verbose_name='Nature du colis'),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Créé le'),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='date_depot',
            field=models.DateField(blank=True, null=True, verbose_name='Date de dépot'),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='date_reception',
            field=models.DateField(blank=True, null=True, verbose_name='Date de réception'),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commandes_drivers', to=settings.AUTH_USER_MODEL, verbose_name='Conducteur'),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='insurance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='insurance', to='commandes.Insurance', verbose_name='Assurance'),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='numero_commande',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='N° Commande'),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commandes.Package', verbose_name="Package d'envoi"),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='status',
            field=models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='Etat'),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Modifié le'),
        ),
        migrations.AlterField(
            model_name='package',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Créé le'),
        ),
        migrations.AlterField(
            model_name='package',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Modifié le'),
        ),
        migrations.AlterField(
            model_name='tranche',
            name='commission',
            field=models.FloatField(default=0, verbose_name='Commission'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='tranche',
            constraint=models.UniqueConstraint(fields=('package', 'min_weight', 'max_weight', 'price'), name='tranche_unique'),
        ),
    ]

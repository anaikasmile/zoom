# Generated by Django 2.2.13 on 2020-08-16 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agences', '0009_auto_20200808_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicules',
            name='etat',
            field=models.TextField(blank=True, null=True, verbose_name='Etat'),
        ),
        migrations.AlterField(
            model_name='vehicules',
            name='nb_place',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nb places'),
        ),
        migrations.AlterField(
            model_name='vehicules',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='agences.TypeVehicules', verbose_name='Type *'),
        ),
    ]

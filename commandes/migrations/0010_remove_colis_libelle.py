# Generated by Django 2.2.13 on 2020-07-04 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commandes', '0009_colis_libelle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='colis',
            name='libelle',
        ),
    ]

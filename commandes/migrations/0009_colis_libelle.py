# Generated by Django 2.2.13 on 2020-07-04 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commandes', '0008_auto_20200704_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='colis',
            name='libelle',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Nature'),
        ),
    ]

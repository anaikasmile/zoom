# Generated by Django 2.2.13 on 2020-08-01 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commandes', '0020_facture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facture',
            name='link_facture',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Lien facture'),
        ),
    ]
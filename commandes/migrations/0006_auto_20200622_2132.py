# Generated by Django 2.2.13 on 2020-06-22 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commandes', '0005_colis_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colis',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='observation',
            field=models.TextField(blank=True, null=True, verbose_name='Remarques'),
        ),
    ]
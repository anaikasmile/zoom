# Generated by Django 2.2.13 on 2020-07-28 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geolocalisation', '0002_auto_20200724_2340'),
        ('agences', '0007_auto_20200724_2340'),
    ]

    operations = [
        migrations.CreateModel(
            name='Societe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nom *')),
                ('addresses', models.TextField(blank=True, null=True, verbose_name='Adresse')),
                ('tel', models.CharField(blank=True, max_length=200, null=True, verbose_name='Tél')),
                ('email', models.CharField(blank=True, max_length=200, null=True, verbose_name='Email')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='agences')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Créé le')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modifié le')),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='geolocalisation.District', verbose_name='Quartier *')),
            ],
        ),
    ]
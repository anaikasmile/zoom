# Generated by Django 2.2.13 on 2020-06-12 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geolocalisation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nom *')),
                ('addresses', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Créé le')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modifié le')),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='geolocalisation.District', verbose_name='Quartier *')),
            ],
        ),
    ]

# Generated by Django 2.2.13 on 2020-08-10 20:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agences', '0009_auto_20200808_2145'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgenceUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Créé le')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Modifié le')),
                ('agence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agences.Agences')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

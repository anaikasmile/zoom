# Generated by Django 2.2.13 on 2020-07-04 11:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agences', '0006_auto_20200704_1146'),
        ('commandes', '0006_auto_20200622_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commandes',
            name='status',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='HistoriqueCommandes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('state', models.PositiveSmallIntegerField()),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Commentaire')),
                ('agence', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agenceHistorique', to='agences.Agences')),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commandeHistorique', to='commandes.Commandes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userHistorique', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

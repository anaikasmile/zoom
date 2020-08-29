# Generated by Django 2.2.13 on 2020-07-28 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commandes', '0015_package'),
    ]

    operations = [
        migrations.AddField(
            model_name='tranche',
            name='package',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='packageTranche', to='commandes.Package', verbose_name="Package d'envoi"),
            preserve_default=False,
        ),
    ]
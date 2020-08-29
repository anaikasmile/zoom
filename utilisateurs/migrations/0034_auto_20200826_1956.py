# Generated by Django 2.2.13 on 2020-08-26 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agences', '0011_auto_20200826_1956'),
        ('utilisateurs', '0033_auto_20200824_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='agence',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agencePerson', to='agences.Agences'),
        ),
        migrations.AlterField(
            model_name='identity',
            name='contact_tel',
            field=models.CharField(blank=True, help_text='', max_length=50, verbose_name='Tél'),
        ),
    ]

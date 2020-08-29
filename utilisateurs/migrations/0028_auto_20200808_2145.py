# Generated by Django 2.2.13 on 2020-08-08 21:45

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0027_auto_20200807_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identity',
            name='contact_tel',
            field=models.CharField(blank=True, help_text='', max_length=50, verbose_name='Tél'),
        ),
        migrations.AlterField(
            model_name='person',
            name='tel',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='90 00 00 00', max_length=50, region=None, unique=True, verbose_name='Téléphone'),
        ),
    ]

# Generated by Django 2.2.13 on 2020-08-03 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0025_auto_20200801_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identity',
            name='contact_tel',
            field=models.CharField(blank=True, help_text='', max_length=50, verbose_name='Tél'),
        ),
    ]

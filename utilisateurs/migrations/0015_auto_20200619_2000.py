# Generated by Django 2.2.13 on 2020-06-19 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0014_auto_20200616_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='job',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Profession'),
        ),
        migrations.AlterField(
            model_name='identity',
            name='contact_tel',
            field=models.CharField(blank=True, help_text='', max_length=50, verbose_name='Tél'),
        ),
    ]

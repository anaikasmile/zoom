# Generated by Django 2.2.13 on 2020-06-16 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0010_auto_20200616_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identity',
            name='contact_tel',
            field=models.CharField(blank=True, help_text='', max_length=50, verbose_name='Tél'),
        ),
    ]

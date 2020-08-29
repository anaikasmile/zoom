# Generated by Django 2.2.13 on 2020-08-26 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0038_auto_20200826_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='is_agent',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='agent',
            name='is_driver',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='agent',
            name='is_staff_member',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='agent',
            name='contact_tel',
            field=models.CharField(blank=True, help_text='', max_length=50, verbose_name='Tél'),
        ),
        migrations.AlterField(
            model_name='identity',
            name='contact_tel',
            field=models.CharField(blank=True, help_text='', max_length=50, verbose_name='Tél'),
        ),
    ]
# Generated by Django 2.0.5 on 2018-05-28 23:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discordbot', '0066_remove_wfsettings_corrosive'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wfsettings',
            name='exilus_bp',
        ),
    ]

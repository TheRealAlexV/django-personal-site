# Generated by Django 2.0.2 on 2018-02-20 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discordbot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='discorduser',
            name='poe_profile',
            field=models.TextField(blank=True),
        ),
    ]

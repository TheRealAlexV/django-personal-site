# Generated by Django 2.0.2 on 2018-03-26 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discordbot', '0032_auto_20180322_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discorduser',
            name='blizzard_id',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='discorduser',
            name='poe_profile',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='discorduser',
            name='steam_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
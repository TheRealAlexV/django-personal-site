# Generated by Django 2.0.2 on 2018-02-20 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discordbot', '0003_poecharacter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discorduser',
            name='poe_profile',
            field=models.TextField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='poecharacter',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discordbot.DiscordUser', to_field='poe_profile'),
        ),
    ]

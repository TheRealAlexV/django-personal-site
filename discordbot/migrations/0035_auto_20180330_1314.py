# Generated by Django 2.0.2 on 2018-03-30 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discordbot', '0034_discorduser_test_bool'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discorduser',
            name='admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='discorduser',
            name='mod_group',
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 2.0.2 on 2018-03-30 16:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discordbot', '0040_auto_20180330_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discorduser',
            name='blizzard_id',
            field=models.TextField(blank=True, default='', help_text='Example: Username-0000', null=True, verbose_name='Blizzard Tag'),
        ),
        migrations.AlterField(
            model_name='discorduser',
            name='steam_id',
            field=models.CharField(blank=True, default='', help_text='17 characters, digits only.', max_length=17, null=True, validators=[django.core.validators.RegexValidator('^\\d{1,17}$')], verbose_name='Steam ID'),
        ),
    ]

# Generated by Django 2.0.2 on 2018-04-23 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discordbot', '0049_auto_20180423_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='discorduser',
            name='warframe_resources',
            field=models.TextField(blank=True, help_text='Comma separeted words', verbose_name='Desired resources'),
        ),
    ]
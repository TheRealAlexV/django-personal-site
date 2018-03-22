# Generated by Django 2.0.2 on 2018-03-21 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discordbot', '0012_auto_20180321_0709'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscordSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField(blank=True, null=True, unique=True)),
                ('value', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'discordbot_settings',
            },
        ),
    ]

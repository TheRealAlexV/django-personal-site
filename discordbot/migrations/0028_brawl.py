# Generated by Django 2.0.2 on 2018-03-22 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discordbot', '0027_delete_brawl'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brawl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('names', models.TextField(blank=True, null=True)),
                ('actions', models.TextField(blank=True, null=True)),
                ('victims', models.TextField(blank=True, null=True)),
                ('tools', models.TextField(blank=True, null=True)),
                ('actions2', models.TextField(blank=True, null=True)),
                ('places', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'discord_brawl',
            },
        ),
    ]

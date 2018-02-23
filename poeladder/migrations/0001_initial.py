# Generated by Django 2.0.2 on 2018-02-21 02:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('discordbot', '0011_auto_20180221_0427'),
    ]

    operations = [
        migrations.CreateModel(
            name='PoeCharacter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(unique=True)),
                ('ascendancy', models.TextField(max_length=30)),
                ('level', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'poeladder_characters',
            },
        ),
        migrations.CreateModel(
            name='PoeLeague',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('url', models.URLField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'poeladder_leagues',
            },
        ),
        migrations.AddField(
            model_name='poecharacter',
            name='league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poeladder.PoeLeague'),
        ),
        migrations.AddField(
            model_name='poecharacter',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discordbot.DiscordUser'),
        ),
    ]

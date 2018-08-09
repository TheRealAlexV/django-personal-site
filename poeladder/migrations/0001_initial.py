# Generated by Django 2.0.2 on 2018-08-09 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('discordbot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PoeActiveGem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('icon', models.URLField(blank=True, null=True)),
            ],
            options={
                'db_table': 'poeladder_gems',
                'verbose_name_plural': 'Gems',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='PoeCharacter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(unique=True)),
                ('class_name', models.TextField(max_length=30)),
                ('class_id', models.IntegerField(blank=True, null=True)),
                ('ascendancy_id', models.IntegerField(blank=True, null=True)),
                ('level', models.IntegerField(blank=True, null=True)),
                ('experience', models.BigIntegerField(blank=True, null=True)),
                ('gems', models.ManyToManyField(to='poeladder.PoeActiveGem')),
            ],
            options={
                'db_table': 'poeladder_characters',
                'verbose_name_plural': 'Characters',
            },
        ),
        migrations.CreateModel(
            name='PoeInfo',
            fields=[
                ('key', models.TextField(primary_key=True, serialize=False, unique=True)),
                ('value', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'poeladder_info',
            },
        ),
        migrations.CreateModel(
            name='PoeLeague',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('url', models.URLField(blank=True, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('slug', models.SlugField(default=None, null=True)),
            ],
            options={
                'db_table': 'poeladder_leagues',
                'verbose_name_plural': 'Leagues',
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

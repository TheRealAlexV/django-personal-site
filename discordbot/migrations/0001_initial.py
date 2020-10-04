# Generated by Django 2.0.2 on 2018-08-09 13:32

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brawl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('action', models.TextField(blank=True, null=True)),
                ('victim', models.TextField(blank=True, null=True)),
                ('tool', models.TextField(blank=True, null=True)),
                ('action2', models.TextField(blank=True, null=True)),
                ('place', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'discord_brawl',
            },
        ),
        migrations.CreateModel(
            name='DiscordLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=20, null=True, unique=True)),
                ('url', models.URLField()),
            ],
            options={
                'db_table': 'discord_links',
                'verbose_name_plural': 'Discord Links',
            },
        ),
        migrations.CreateModel(
            name='DiscordPicture',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('pid', models.IntegerField(db_column='pID', default=0)),
                ('url', models.URLField(unique=True)),
                ('date', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'discord_pictures',
            },
        ),
        migrations.CreateModel(
            name='DiscordSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=20, null=True, unique=True)),
                ('value', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'discord_settings',
                'verbose_name_plural': 'Discord Settings',
            },
        ),
        migrations.CreateModel(
            name='DiscordUser',
            fields=[
                ('token', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('id', models.IntegerField(blank=True, help_text='Required. 18 characters, digits only.', max_length=18, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.RegexValidator('^\\d{1,18}$')], verbose_name='Discord ID')),
                ('display_name', models.TextField(help_text='Current discord display name', max_length=40, verbose_name='Username')),
                ('steam_id', models.CharField(blank=True, default='', help_text='17 characters, digits only.', max_length=17, validators=[django.core.validators.RegexValidator('^\\d{1,17}$')], verbose_name='Steam ID')),
                ('blizzard_id', models.TextField(blank=True, default='', help_text='Example: Username-0000', verbose_name='Blizzard Tag')),
                ('poe_profile', models.TextField(blank=True, default='', verbose_name='PoE Account')),
                ('admin', models.BooleanField(default=False, help_text='User can execute @admin commands')),
                ('mod_group', models.BooleanField(default=False, help_text='User can execute @mod commands', verbose_name='Moderator')),
                ('avatar_url', models.URLField(blank=True, default=None, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'discord_users',
                'verbose_name_plural': 'Discord Users',
            },
        ),
        migrations.CreateModel(
            name='Gachi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField(blank=True, default=0, null=True)),
                ('url', models.URLField(blank=True, null=True, unique=True)),
            ],
            options={
                'db_table': 'discord_gachi',
            },
        ),
        migrations.CreateModel(
            name='WFAlert',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('announced', models.BooleanField(default=False)),
                ('content', models.TextField()),
                ('keywords', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'discord_alerts',
                'verbose_name_plural': 'Warframe Alerts',
                'verbose_name': 'Warframe Alert',
            },
        ),
        migrations.CreateModel(
            name='WFSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nitain_extract', models.BooleanField(default=False)),
                ('orokin_cell', models.BooleanField(default=False)),
                ('orokin_reactor_bp', models.BooleanField(default=False)),
                ('orokin_catalyst_bp', models.BooleanField(default=False)),
                ('tellurium', models.BooleanField(default=False)),
                ('forma_bp', models.BooleanField(default=False)),
                ('exilus_ap', models.BooleanField(default=False)),
                ('kavat', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'discord_wf_settings',
            },
        ),
        migrations.CreateModel(
            name='Wisdom',
            fields=[
                ('id', models.IntegerField(blank=True, primary_key=True, serialize=False)),
                ('pid', models.IntegerField(db_column='pID', default=0)),
                ('text', models.TextField(unique=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discordbot.DiscordUser', verbose_name='discord user')),
            ],
            options={
                'db_table': 'discord_wisdoms',
            },
        ),
        migrations.AddField(
            model_name='discorduser',
            name='wf_settings',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='discordbot.WFSettings'),
        ),
    ]

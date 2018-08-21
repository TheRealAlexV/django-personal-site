# Generated by Django 2.0.2 on 2018-08-19 07:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wowstats', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WOWSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_2v2', models.BooleanField(default=True)),
                ('track_3v3', models.BooleanField(default=True)),
                ('track_rbg', models.BooleanField(default=True)),
                ('track_skirmish', models.BooleanField(default=True)),
                ('track_unknown', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'wow_settings',
            },
        ),
        migrations.AddField(
            model_name='wowaccount',
            name='region',
            field=models.CharField(choices=[('eu', 'Europe'), ('us', 'United States')], default='eu', max_length=2),
        ),
    ]
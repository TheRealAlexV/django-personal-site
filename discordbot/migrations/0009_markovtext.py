# Generated by Django 2.2.6 on 2019-10-10 20:08

from django.db import migrations, models


def create_models(apps, _):
    MarkovText = apps.get_model("discordbot", "MarkovText")
    MarkovText.objects.create(
        text='.',
        last_update=None
    )


def remove_models(apps, _):
    MarkovText = apps.get_model("discordbot", "MarkovText")
    MarkovText.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('discordbot', '0008_counter_countergroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarkovText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('last_update', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.RunPython(create_models, reverse_code=remove_models)
    ]

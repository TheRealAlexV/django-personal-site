# Generated by Django 2.2.6 on 2019-11-13 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discordbot', '0009_markovtext'),
    ]

    operations = [
        migrations.AddField(
            model_name='markovtext',
            name='key',
            field=models.CharField(default='default', help_text='Unique identifier', max_length=200, unique=True),
            preserve_default=False,
        ),
    ]

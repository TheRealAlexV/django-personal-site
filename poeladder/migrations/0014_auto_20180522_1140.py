# Generated by Django 2.0.5 on 2018-05-22 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    operations = [
        migrations.CreateModel(
            name='PoeActiveSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('icon', models.URLField(blank=True, null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.RemoveField(
            model_name='poecharacter',
            name='main_skills',
        ),
        migrations.AddField(
            model_name='poecharacter',
            name='main_skills',
            field=models.ManyToManyField(to='poeladder.PoeActiveSkill'),
        ),
    ]

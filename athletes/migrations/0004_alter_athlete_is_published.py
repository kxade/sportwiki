# Generated by Django 4.2.5 on 2023-10-13 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('athletes', '0003_alter_athlete_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athlete',
            name='is_published',
            field=models.BooleanField(choices=[(0, 'Черновик'), (1, 'Опубликовано')], default=0),
        ),
    ]
# Generated by Django 2.1.5 on 2019-04-20 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_sensor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='sensor_id',
            field=models.CharField(max_length=60, unique=True),
        ),
    ]

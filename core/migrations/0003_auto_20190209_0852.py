# Generated by Django 2.1.5 on 2019-02-09 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190209_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccessrequest',
            name='is_allowed',
            field=models.NullBooleanField(),
        ),
    ]

# Generated by Django 2.1.5 on 2019-03-16 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0007_auto_20190312_0613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='assets',
            field=models.CharField(max_length=500),
        ),
    ]

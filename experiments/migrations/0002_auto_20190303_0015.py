# Generated by Django 2.1.5 on 2019-03-02 23:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='active_flag',
            field=models.PositiveIntegerField(choices=[(0, 'inactive'), (1, 'active')], default=1),
        ),
        migrations.AddField(
            model_name='experiment',
            name='end_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='experiment',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, 'created'), (1, 'running'), (2, 'completed')], default=0),
        ),
    ]

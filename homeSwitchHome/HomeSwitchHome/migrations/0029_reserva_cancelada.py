# Generated by Django 2.2.1 on 2019-07-13 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeSwitchHome', '0028_auto_20210712_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='cancelada',
            field=models.BooleanField(default=False),
        ),
    ]

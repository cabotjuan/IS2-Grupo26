# Generated by Django 2.2.1 on 2019-05-18 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeSwitchHome', '0005_auto_20190517_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='semana',
            name='habilitada',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='subasta',
            name='fecha_inicio',
            field=models.DateField(blank=True),
        ),
    ]
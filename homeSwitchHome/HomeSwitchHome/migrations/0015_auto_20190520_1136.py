# Generated by Django 2.2.1 on 2019-05-20 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeSwitchHome', '0014_auto_20190519_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foto',
            name='archivo',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
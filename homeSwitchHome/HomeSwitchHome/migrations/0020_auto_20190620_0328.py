# Generated by Django 2.2.1 on 2019-06-20 06:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HomeSwitchHome', '0019_auto_20190619_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='usuario',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

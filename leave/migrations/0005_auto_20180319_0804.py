# Generated by Django 2.0.3 on 2018-03-19 08:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0004_auto_20180315_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='applicant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 3.1.2 on 2020-11-02 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0007_auto_20201102_0154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='address',
        ),
        migrations.RemoveField(
            model_name='application',
            name='reason',
        ),
        migrations.AlterField(
            model_name='application',
            name='typeOfLeave',
            field=models.CharField(choices=[('EL', 'Earned Leave'), ('HPL', 'Half Pay Leave'), ('OT', 'Other Leave')], max_length=3),
        ),
    ]

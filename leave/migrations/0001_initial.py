# Generated by Django 2.0.1 on 2018-03-15 12:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('reason', models.TextField()),
                ('address', models.TextField()),
                ('submitted', models.BooleanField(default=False)),
                ('recommended', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('typeOfLeave', models.CharField(choices=[('EL', 'Earned Leave'), ('HPL', 'Half Pay Leave'), ('OT', 'Other Leave')], default='OT', max_length=3)),
                ('prefix', models.IntegerField(default=0)),
                ('suffix', models.IntegerField(default=0)),
                ('availLTC', models.BooleanField(default=False)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 2.2.4 on 2019-10-15 10:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patientfirstname', models.CharField(max_length=50)),
                ('patientlastname', models.CharField(max_length=50)),
                ('patientaddress', models.CharField(max_length=50)),
                ('patientemail', models.EmailField(max_length=25)),
                ('patientpassword', models.CharField(max_length=10)),
                ('patientnumber', models.IntegerField()),
                ('citizennumber', models.IntegerField()),
                ('login_date', models.DateField(default=datetime.date.today)),
                ('patientdob', models.DateField()),
                ('patientprofile', models.ImageField(upload_to='patientimage')),
                ('patientpin', models.CharField(default='abs', max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Citizennumber', models.IntegerField()),
                ('Subject', models.CharField(max_length=100)),
                ('Patientfile', models.FileField(upload_to='Report')),
                ('Description', models.CharField(max_length=200)),
                ('Hospitalname', models.CharField(default='blank', max_length=50)),
                ('uploaddate', models.DateField(default=datetime.date.today)),
            ],
        ),
    ]
# Generated by Django 2.2.4 on 2019-10-04 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0004_auto_20191004_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='hospitalnumber',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='hospitalpan',
            field=models.IntegerField(),
        ),
    ]
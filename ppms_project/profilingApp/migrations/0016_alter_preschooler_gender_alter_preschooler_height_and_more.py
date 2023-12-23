# Generated by Django 4.1.2 on 2022-10-27 15:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profilingApp', '0015_preschooler_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preschooler',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='preschooler',
            name='height',
            field=models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(45.0), django.core.validators.MaxValueValidator(120.0)]),
        ),
        migrations.AlterField(
            model_name='preschooler',
            name='weight',
            field=models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(28.0)]),
        ),
    ]
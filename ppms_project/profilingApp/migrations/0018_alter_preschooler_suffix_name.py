# Generated by Django 4.1.2 on 2022-10-27 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profilingApp', '0017_preschooler_date_measured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preschooler',
            name='suffix_name',
            field=models.CharField(default='N/A', max_length=100),
        ),
    ]
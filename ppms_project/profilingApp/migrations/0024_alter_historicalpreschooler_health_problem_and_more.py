# Generated by Django 4.1.2 on 2022-11-07 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profilingApp', '0023_historicalpreschooler_historicallog_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpreschooler',
            name='health_problem',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='datetime_log',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='preschooler',
            name='health_problem',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.DeleteModel(
            name='HistoricalLog',
        ),
    ]

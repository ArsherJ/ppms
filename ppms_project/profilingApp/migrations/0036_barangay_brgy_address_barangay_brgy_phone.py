# Generated by Django 4.1.2 on 2022-11-18 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profilingApp', '0035_barangayhealthworker'),
    ]

    operations = [
        migrations.AddField(
            model_name='barangay',
            name='brgy_address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='barangay',
            name='brgy_phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

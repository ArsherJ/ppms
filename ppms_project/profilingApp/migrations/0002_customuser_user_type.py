# Generated by Django 4.0.1 on 2022-09-05 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profilingApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('Choose User Type', 'Choose User Type'), ('BHW', 'Barangay Health Worker'), ('P/G', 'Parent/Guardian')], default='Choose User Type', max_length=100),
        ),
    ]

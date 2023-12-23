# Generated by Django 4.1.2 on 2022-10-21 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profilingApp', '0010_delete_preschooler'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preschooler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(max_length=100)),
                ('suffix_name', models.CharField(max_length=100)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profilingApp.parent')),
            ],
        ),
    ]
# Generated by Django 5.1 on 2024-12-12 03:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_alter_project_is_open'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='treat_count',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]

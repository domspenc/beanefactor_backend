# Generated by Django 5.1 on 2024-12-05 02:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_category_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='project',
        ),
        migrations.AddField(
            model_name='comment',
            name='pledge',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='projects.treatpledge'),
            preserve_default=False,
        ),
    ]
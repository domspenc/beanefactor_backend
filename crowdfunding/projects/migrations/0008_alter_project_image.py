# Generated by Django 5.1 on 2024-12-07 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_alter_project_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.URLField(blank=True, default='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.redbubble.com%2Fi%2Fkids-t-shirt%2FCheeky-Italian-Greyhound-Cartoon-Style-Pet-Art-by-NinosDelViento%2F144984081.MZ153&psig=AOvVaw3htc2aVellqSjNxOeqd4ku&ust=1733644491238000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCMDvxZSXlYoDFQAAAAAdAAAAABAE', max_length=2000, null=True),
        ),
    ]

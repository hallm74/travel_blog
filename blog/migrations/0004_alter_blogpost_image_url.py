# Generated by Django 5.1.4 on 2025-01-03 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_blogpost_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image_url',
            field=models.URLField(blank=True, help_text='URL of the image fetched from Unsplash.', max_length=500, null=True),
        ),
    ]
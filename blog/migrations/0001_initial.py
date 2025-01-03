# Generated by Django 5.1.4 on 2025-01-03 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the tag.', max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(default='AI', help_text='Name of the content creator, default is AI.', max_length=100)),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='Date and time when the post is published.')),
                ('content', models.TextField(help_text='Main content of the blog post, generated by AI.')),
                ('image_url', models.URLField(blank=True, help_text='URL of the image fetched from Unsplash.', null=True)),
                ('description', models.CharField(blank=True, help_text='Short description or summary of the post.', max_length=500)),
                ('tags', models.ManyToManyField(blank=True, help_text='Tags related to the blog post.', to='blog.tag')),
            ],
        ),
    ]

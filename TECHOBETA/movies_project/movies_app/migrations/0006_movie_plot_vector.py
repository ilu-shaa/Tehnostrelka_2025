# Generated by Django 4.2 on 2025-02-26 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_app', '0005_movie_author_movie_reviews_movie_year_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='plot_vector',
            field=models.TextField(blank=True, null=True),
        ),
    ]

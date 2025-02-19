from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    user_tags = models.CharField(max_length=200)
    reviews = models.JSONField()
    author = models.CharField(max_length=200)
    plot = models.TextField()
    poster = models.ImageField(upload_to='posters/')

    def __str__(self):
        return self.title
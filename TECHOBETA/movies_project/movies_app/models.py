from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.PositiveSmallIntegerField()
    user_tags = models.CharField(max_length=255)   # Можно хранить как текст
    reviews = models.TextField()                   # Будем хранить JSON-строку
    author = models.CharField(max_length=255)      # Режиссёр / автор
    plot = models.TextField()                      # Описание
    poster = models.CharField(max_length=255)      # Имя файла постера

    def __str__(self):
        return self.title
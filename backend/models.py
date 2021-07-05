from django.db import models


class FilmManager(models.Manager):

    def get_queryset(self):

        return super().get_queryset()


class Film(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=4)
    rating = models.CharField(max_length=5)
    image = models.CharField(max_length=255)
    filmId = models.IntegerField(unique=True, null=True)
    objects = FilmManager()

    def __str__(self):
        return self.name

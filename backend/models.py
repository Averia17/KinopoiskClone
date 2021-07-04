from django.db import models
from .services import get_top_films


class FilmManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def all(self):
        if not self.get_queryset().exists():
            for film in get_top_films():
                f = Film(name=film.get('nameRu'),
                         year=film.get('year'),
                         rating=film.get('rating'),
                         image=film.get('posterUrl'),
                         filmId=film.get('filmId')
                         )
                f.save()
        return self.get_queryset()


class Film(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=4)
    rating = models.CharField(max_length=5)
    image = models.CharField(max_length=255)
    filmId = models.IntegerField(unique=True)
    objects = FilmManager()

    def __str__(self):
        return self.name

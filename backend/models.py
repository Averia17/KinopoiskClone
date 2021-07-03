from django.db import models


class Film(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=4)
    rating = models.CharField(max_length=5)
    image = models.CharField(max_length=255)

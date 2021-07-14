from django.db import models


class FilmManager(models.Manager):

    def get_queryset(self):

        return super().get_queryset()


class Genre(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Country(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Staff(models.Model):
    nameRu = models.CharField(max_length=100, null=True, blank=True)
    staffId = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    professionText = models.CharField(max_length=55, null=True, blank=True)
    professionKey = models.CharField(max_length=55, null=True, blank=True)
    birthday = models.CharField(max_length=55, null=True, blank=True)
    death = models.CharField(max_length=55, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    growth = models.IntegerField(null=True, blank=True)
    profession = models.CharField(max_length=55, null=True, blank=True)


    def __str__(self):
        return self.nameRu


class Film(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=4)
    rating = models.CharField(max_length=5)
    image = models.CharField(max_length=255)
    filmId = models.IntegerField(null=True, blank=True)
    slogan = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    filmLength = models.CharField(max_length=20, null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)
    ratingAgeLimits = models.CharField(max_length=20, null=True, blank=True)
    premiereRu = models.CharField(max_length=20, null=True, blank=True)
    #distributors = models.CharField(max_length=20, null=True, blank=True)
    premiereWorld = models.CharField(max_length=20, null=True, blank=True)
    premiereDigital = models.CharField(max_length=20, null=True, blank=True)
    premiereWorldCountry = models.CharField(max_length=20, null=True, blank=True)
    #distributorRelease = models.CharField(max_length=20, null=True, blank=True)
    countries = models.ManyToManyField(Country)
    genres = models.ManyToManyField(Genre)
    facts = models.JSONField(default=list)
    budget = models.CharField(max_length=30, null=True, blank=True)
    grossRu = models.IntegerField(null=True, blank=True)
    grossUsa = models.IntegerField(null=True, blank=True)
    grossWorld = models.IntegerField(null=True, blank=True)
    trailers = models.JSONField(default=list)
    teasers = models.JSONField(default=list)

    staff = models.ManyToManyField(Staff)
    objects = FilmManager()

    def __str__(self):
        return self.name




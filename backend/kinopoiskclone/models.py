import json

from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from pytils.translit import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    saved_films = models.ManyToManyField('Film')

    def __str__(self):
        return self.user.username


class FilmManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()


class Genre(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)

    def save(self, *args, **kwargs):
        if not len(self.slug.strip()):
            self.slug = slugify(self.title, allow_unicode=True)

        _slug = self.slug
        _count = 1

        while True:
            try:
                Genre.objects.all().exclude(pk=self.pk).get(slug=_slug)
            except MultipleObjectsReturned:
                pass
            except ObjectDoesNotExist:
                break
            _slug = "%s-%s" % (self.slug, _count)
            _count += 1

        self.slug = _slug

        super(Genre, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def toJSON(self):
        return json.dumps(self.title)


class Country(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)

    def save(self, *args, **kwargs):
        if not len(self.slug.strip()):
            self.slug = slugify(self.title, allow_unicode=True)

        _slug = self.slug
        _count = 1

        while True:
            try:
                Country.objects.all().exclude(pk=self.pk).get(slug=_slug)
            except MultipleObjectsReturned:
                pass
            except ObjectDoesNotExist:
                break
            _slug = "%s-%s" % (self.slug, _count)
            _count += 1

        self.slug = _slug

        super(Country, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Staff(models.Model):
    nameRu = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    staffId = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=511, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    professionText = models.CharField(max_length=64, null=True, blank=True)
    professionKey = models.CharField(max_length=64, null=True, blank=True)
    birthday = models.CharField(max_length=64, null=True, blank=True)
    death = models.CharField(max_length=64, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    growth = models.IntegerField(null=True, blank=True)
    profession = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nameRu


class Film(models.Model):
    name = models.CharField(max_length=510)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=510)
    year = models.CharField(max_length=32)
    rating = models.FloatField(null=True, blank=True)
    image = models.CharField(max_length=255)
    filmId = models.IntegerField(unique=True, null=True, blank=True)
    slogan = models.CharField(max_length=510, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    filmLength = models.CharField(max_length=64, null=True, blank=True)
    type = models.CharField(max_length=64, null=True, blank=True)
    ratingAgeLimits = models.CharField(max_length=64, null=True, blank=True)
    premiereRu = models.CharField(max_length=64, null=True, blank=True)
    # distributors = models.CharField(max_length=20, null=True, blank=True)
    premiereWorld = models.CharField(max_length=64, null=True, blank=True)
    premiereDigital = models.CharField(max_length=64, null=True, blank=True)
    premiereWorldCountry = models.CharField(max_length=64, null=True, blank=True)
    # distributorRelease = models.CharField(max_length=20, null=True, blank=True)
    countries = models.ManyToManyField(Country)
    genres = models.ManyToManyField(Genre)
    facts = models.JSONField(default=list)
    budget = models.CharField(max_length=64, null=True, blank=True)
    grossRu = models.BigIntegerField(null=True, blank=True)
    grossUsa = models.BigIntegerField(null=True, blank=True)
    grossWorld = models.BigIntegerField(null=True, blank=True)
    trailers = models.JSONField(default=list)
    teasers = models.JSONField(default=list)

    staff = models.ManyToManyField(Staff)
    objects = FilmManager()

    class Meta:
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['id', 'name', 'year', 'image']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not len(self.slug.strip()):
            self.slug = slugify(self.name, allow_unicode=True)

        _slug = self.slug
        _count = 1

        while True:
            try:
                Film.objects.all().exclude(pk=self.pk).get(slug=_slug)
            except MultipleObjectsReturned:
                pass
            except ObjectDoesNotExist:
                break
            _slug = "%s-%s" % (self.slug, _count)
            _count += 1

        self.slug = _slug

        super(Film, self).save(*args, **kwargs)


# class Serial(Film):
#     episodes =

#
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()

# docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' dev-db
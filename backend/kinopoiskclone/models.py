import json

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from pytils.translit import slugify
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("The email must be set")
        if not password:
            raise ValueError("The password must be set")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    saved_books = models.ManyToManyField('Film')
    email = models.EmailField(db_index=True, unique=True, default=None, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "email"

    objects = MyUserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


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
    vector_name = SearchVectorField(null=True)

    staff = models.ManyToManyField(Staff)
    objects = FilmManager()

    class Meta:
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['id', 'name', 'year', 'image']),
            GinIndex(fields=[
                "vector_name",
            ]),
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
# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#     instance.userprofile.save()

# docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' dev-db

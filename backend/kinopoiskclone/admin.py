from django.contrib import admin

# Register your models here.
from kinopoiskclone.models import Film, Staff, Genre, Country

admin.site.register(Film)
admin.site.register(Staff)
admin.site.register(Genre)
admin.site.register(Country)

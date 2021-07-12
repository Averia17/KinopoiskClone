from django.contrib import admin

# Register your models here.
from backend.models import Film, Staff, Genre

admin.site.register(Film)
admin.site.register(Staff)
admin.site.register(Genre)

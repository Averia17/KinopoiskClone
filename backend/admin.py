from django.contrib import admin

# Register your models here.
from backend.models import Film, Staff

admin.site.register(Film)
admin.site.register(Staff)

"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from kinopoiskclone.views import main_page, film_detail, staff_detail, serials, films, genre_detail, country_detail

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', main_page),
    path('films/<int:id>/', film_detail),
    path('staff/<int:id>/', staff_detail),
    path('serials/<int:id>/', serials),
    path('films/', films),
    path('serials/', serials),
    path('genres/<str:slug>', genre_detail),
    path('countries/<str:slug>', country_detail),

    path('api/', include('kinopoiskclone.api.urls'))
]

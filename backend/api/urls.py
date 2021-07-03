from django.urls import path

from .views import MainPageView


urlpatterns = [
    path('top-films/', MainPageView.as_view(), name='top-films')
]
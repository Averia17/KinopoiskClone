from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import FilmsViewSet

router = SimpleRouter()

router.register('films', FilmsViewSet, basename='films')

urlpatterns = []
urlpatterns += router.urls

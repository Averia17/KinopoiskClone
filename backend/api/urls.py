from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import FilmsViewSet, StaffViewSet, SerialsViewSet

router = SimpleRouter()

router.register('films', FilmsViewSet, basename='films')
router.register('serials', SerialsViewSet, basename='serials')
router.register('staff', StaffViewSet, basename='staff')

urlpatterns = []
urlpatterns += router.urls

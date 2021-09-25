from rest_framework.routers import SimpleRouter

from .views import FilmsViewSet, StaffViewSet, SerialsViewSet, GenresViewSet, CountriesViewSet, AllMoviesViewSet

router = SimpleRouter()

router.register('films', FilmsViewSet, basename='films')
router.register('genres', GenresViewSet, basename='genres')
router.register('countries', CountriesViewSet, basename='countries')
router.register('serials', SerialsViewSet, basename='serials')
router.register('staff', StaffViewSet, basename='staff')
router.register('movies', AllMoviesViewSet, basename='movies')

urlpatterns = []
urlpatterns += router.urls

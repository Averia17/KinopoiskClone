from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import FilmsViewSet, StaffViewSet, SerialsViewSet, GenresViewSet, CountriesViewSet, AllMoviesViewSet, \
    UserProfileViewSet, FavoritesViewSet

router = SimpleRouter()

router.register('films', FilmsViewSet, basename='films')
router.register('genres', GenresViewSet, basename='genres')
router.register('countries', CountriesViewSet, basename='countries')
router.register('serials', SerialsViewSet, basename='serials')
router.register('staff', StaffViewSet, basename='staff')
router.register('movies', AllMoviesViewSet, basename='movies')
router.register('users', UserProfileViewSet, basename='users')
router.register('favorites', FavoritesViewSet, basename='favorites')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token-verify/', TokenVerifyView.as_view(), name='token-verify')
]
urlpatterns += router.urls

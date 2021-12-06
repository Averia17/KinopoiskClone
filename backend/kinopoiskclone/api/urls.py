from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import FilmsViewSet, StaffViewSet, SerialsViewSet, GenresViewSet, CountriesViewSet, AllMoviesViewSet, \
    FavoritesViewSet, RegisterUser, UserViewSet, TestSearch

router = SimpleRouter()

router.register('films', FilmsViewSet, basename='films')
router.register('genres', GenresViewSet, basename='genres')
router.register('countries', CountriesViewSet, basename='countries')
router.register('serials', SerialsViewSet, basename='serials')
router.register('staff', StaffViewSet, basename='staff')
router.register('movies', AllMoviesViewSet, basename='movies')
router.register('users', UserViewSet, basename='users')
router.register('favorites', FavoritesViewSet, basename='favorites')

urlpatterns = [
    path("register/", RegisterUser.as_view(), name="register_user"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token-verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('search/', TestSearch.as_view(), name='search')
]
urlpatterns += router.urls

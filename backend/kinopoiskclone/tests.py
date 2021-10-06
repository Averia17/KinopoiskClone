from decouple import config
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from kinopoiskclone.models import Film


class BaseTestCase(APITestCase):

    def setUp(self):
        self.email = config('TEST_EMAIL')
        self.username = config('TEST_USERNAME')
        self.password = config('PASSWORD')
        self.user = User.objects.create_user(
            self.username, self.email, self.password)
        self.data = {
            'username': self.username,
            'password': self.password
        }


class UserTestCase(BaseTestCase):
    def test_registration(self):
        data = {
            'username': 'admin',
            'password': 'randomPasswrod123'
        }
        response = self.client.post("/api/auth/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authentication(self):
        response = self.client.post("/api/login/", self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_verification(self):
        response = self.client.post('/api/token-verify/', {'token': 'abc'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class FilmViewSetTestCase(BaseTestCase):
    def test_get_films(self):
        response = self.client.get("/api/films/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.content)
        self.assertNotEqual(Film.objects.all(), 0)


class CountriesViewSetTestCase(BaseTestCase):
    def test_get_countries(self):
        response = self.client.get("/api/countries/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.content)

    def test_get_country_by_name(self):
        response = self.client.get("/api/countries/ssha/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.content)


class GenreViewSetTestCase(BaseTestCase):
    def test_get_genres(self):
        response = self.client.get("/api/genres/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.content)

    def test_get_genre_by_name(self):
        response = self.client.get("/api/genres/drama/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.content)

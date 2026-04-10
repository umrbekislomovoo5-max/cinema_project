from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Genre, Movie
import datetime


class GenreAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.genre = Genre.objects.create(name='Action')

    def test_list_genres(self):
        response = self.client.get('/api/movies/genres/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_genre_unauthenticated(self):
        response = self.client.post('/api/movies/genres/', {'name': 'Drama'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MovieAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.genre = Genre.objects.create(name='Comedy')
        self.movie = Movie.objects.create(
            title='Test Movie',
            duration=120,
            release_date=datetime.date(2024, 1, 1),
        )
        self.movie.genres.add(self.genre)

    def test_list_movies(self):
        response = self.client.get('/api/movies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_genre(self):
        response = self.client.get('/api/movies/?genre=Comedy')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_genre_no_match(self):
        response = self.client.get('/api/movies/?genre=Horror')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

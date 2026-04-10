from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Hall, Seat, Screening
from movies.models import Movie
import datetime


class HallAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hall = Hall.objects.create(name='Hall 1', total_rows=5, seats_per_row=10)

    def test_list_halls(self):
        response = self.client.get('/api/cinema/halls/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_total_seats(self):
        self.assertEqual(self.hall.total_seats, 50)


class ScreeningAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.movie = Movie.objects.create(
            title='Inception',
            duration=148,
            release_date=datetime.date(2010, 7, 16),
        )
        self.hall = Hall.objects.create(name='IMAX', total_rows=10, seats_per_row=15)
        self.screening = Screening.objects.create(
            movie=self.movie,
            hall=self.hall,
            start_time=datetime.datetime(2025, 6, 1, 18, 0, tzinfo=datetime.timezone.utc),
            price='15.00',
        )

    def test_list_screenings(self):
        response = self.client.get('/api/cinema/screenings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_movie(self):
        response = self.client.get(f'/api/cinema/screenings/?movie={self.movie.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_date(self):
        response = self.client.get('/api/cinema/screenings/?date=2025-06-01')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

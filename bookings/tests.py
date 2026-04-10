from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from cinema.models import Hall, Seat, Screening
from movies.models import Movie
from .models import Booking, Ticket
import datetime

User = get_user_model()


class BookingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='booker', password='pass123')
        self.movie = Movie.objects.create(
            title='Avatar',
            duration=162,
            release_date=datetime.date(2009, 12, 18),
        )
        self.hall = Hall.objects.create(name='Hall A', total_rows=3, seats_per_row=4)
        self.seat1 = Seat.objects.create(hall=self.hall, row=1, number=1)
        self.seat2 = Seat.objects.create(hall=self.hall, row=1, number=2)
        self.screening = Screening.objects.create(
            movie=self.movie,
            hall=self.hall,
            start_time=datetime.datetime(2025, 7, 1, 20, 0, tzinfo=datetime.timezone.utc),
            price='12.50',
        )

    def test_booking_requires_auth(self):
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_booking(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'screening': self.screening.pk,
            'seat_ids': [self.seat1.pk, self.seat2.pk],
        }
        response = self.client.post('/api/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 2)

    def test_total_price(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'screening': self.screening.pk,
            'seat_ids': [self.seat1.pk, self.seat2.pk],
        }
        response = self.client.post('/api/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        booking = Booking.objects.first()
        self.assertEqual(booking.total_price, 25)

    def test_user_sees_only_own_bookings(self):
        other_user = User.objects.create_user(username='other', password='pass123')
        Booking.objects.create(user=other_user, screening=self.screening)
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

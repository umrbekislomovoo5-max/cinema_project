from django.db import models
from django.conf import settings
from cinema.models import Screening, Seat


class Booking(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings'
    )
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.screening.price * self.tickets.count()

    def __str__(self):
        return f'Booking #{self.pk} by {self.user} – {self.status}'


class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='tickets')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='tickets')

    class Meta:
        unique_together = ('booking', 'seat')

    def __str__(self):
        return f'Ticket for {self.booking} – {self.seat}'

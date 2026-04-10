from django.db import models
from movies.models import Movie


class Hall(models.Model):
    name = models.CharField(max_length=100)
    total_rows = models.PositiveIntegerField()
    seats_per_row = models.PositiveIntegerField()

    @property
    def total_seats(self):
        return self.total_rows * self.seats_per_row

    def __str__(self):
        return self.name


class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='seats')
    row = models.PositiveIntegerField()
    number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('hall', 'row', 'number')
        ordering = ('row', 'number')

    def __str__(self):
        return f'{self.hall} – Row {self.row} Seat {self.number}'


class Screening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='screenings')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='screenings')
    start_time = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def end_time(self):
        from datetime import timedelta
        return self.start_time + timedelta(minutes=self.movie.duration)

    def __str__(self):
        return f'{self.movie} @ {self.start_time:%Y-%m-%d %H:%M} in {self.hall}'

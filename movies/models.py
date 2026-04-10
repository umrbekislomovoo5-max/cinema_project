from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    release_date = models.DateField()
    genres = models.ManyToManyField(Genre, related_name='movies', blank=True)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    language = models.CharField(max_length=50, default='English')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

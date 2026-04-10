from django.contrib import admin
from .models import Genre, Movie


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'release_date', 'rating', 'language')
    list_filter = ('genres', 'language')
    search_fields = ('title',)
    filter_horizontal = ('genres',)

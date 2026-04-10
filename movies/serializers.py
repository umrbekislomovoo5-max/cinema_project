from rest_framework import serializers
from .models import Genre, Movie


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Genre.objects.all(), write_only=True, source='genres'
    )

    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'description', 'duration', 'release_date',
            'genres', 'genre_ids', 'poster', 'rating', 'language', 'created_at',
        )
        read_only_fields = ('created_at',)

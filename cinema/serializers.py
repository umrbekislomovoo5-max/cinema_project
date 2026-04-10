from rest_framework import serializers
from .models import Hall, Seat, Screening
from movies.serializers import MovieSerializer


class HallSerializer(serializers.ModelSerializer):
    total_seats = serializers.ReadOnlyField()

    class Meta:
        model = Hall
        fields = ('id', 'name', 'total_rows', 'seats_per_row', 'total_seats')


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ('id', 'hall', 'row', 'number')


class ScreeningSerializer(serializers.ModelSerializer):
    movie_detail = MovieSerializer(source='movie', read_only=True)
    hall_detail = HallSerializer(source='hall', read_only=True)
    end_time = serializers.ReadOnlyField()

    class Meta:
        model = Screening
        fields = (
            'id', 'movie', 'movie_detail', 'hall', 'hall_detail',
            'start_time', 'end_time', 'price',
        )

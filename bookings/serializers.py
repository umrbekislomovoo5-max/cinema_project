from rest_framework import serializers
from .models import Booking, Ticket
from cinema.models import Seat
from cinema.serializers import ScreeningSerializer, SeatSerializer


class TicketSerializer(serializers.ModelSerializer):
    seat_detail = SeatSerializer(source='seat', read_only=True)

    class Meta:
        model = Ticket
        fields = ('id', 'seat', 'seat_detail')


class BookingSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
    seat_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Seat.objects.all(), source='seats'
    )
    screening_detail = ScreeningSerializer(source='screening', read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Booking
        fields = (
            'id', 'user', 'screening', 'screening_detail', 'status',
            'tickets', 'seat_ids', 'total_price', 'created_at',
        )
        read_only_fields = ('user', 'status', 'created_at')

    def create(self, validated_data):
        seats = validated_data.pop('seats')
        booking = Booking.objects.create(**validated_data)
        for seat in seats:
            Ticket.objects.create(booking=booking, seat=seat)
        return booking

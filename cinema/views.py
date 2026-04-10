from rest_framework import viewsets, permissions
from .models import Hall, Seat, Screening
from .serializers import HallSerializer, SeatSerializer, ScreeningSerializer


class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SeatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Seat.objects.select_related('hall').all()
    serializer_class = SeatSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        hall_id = self.request.query_params.get('hall')
        if hall_id:
            qs = qs.filter(hall_id=hall_id)
        return qs


class ScreeningViewSet(viewsets.ModelViewSet):
    queryset = Screening.objects.select_related('movie', 'hall').all()
    serializer_class = ScreeningSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        movie_id = self.request.query_params.get('movie')
        if movie_id:
            qs = qs.filter(movie_id=movie_id)
        date = self.request.query_params.get('date')
        if date:
            qs = qs.filter(start_time__date=date)
        return qs

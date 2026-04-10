from rest_framework import viewsets, permissions
from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.select_related('user', 'screening').all()
        return Booking.objects.filter(user=user).select_related('screening')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # Only allow cancellation by the owner
        instance = self.get_object()
        if not self.request.user.is_staff and instance.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied
        serializer.save()

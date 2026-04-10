from rest_framework.routers import DefaultRouter
from .views import HallViewSet, SeatViewSet, ScreeningViewSet

router = DefaultRouter()
router.register('halls', HallViewSet)
router.register('seats', SeatViewSet)
router.register('screenings', ScreeningViewSet)

urlpatterns = router.urls

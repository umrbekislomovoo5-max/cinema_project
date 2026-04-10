from django.contrib import admin
from .models import Hall, Seat, Screening


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_rows', 'seats_per_row', 'total_seats')


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('hall', 'row', 'number')
    list_filter = ('hall',)


@admin.register(Screening)
class ScreeningAdmin(admin.ModelAdmin):
    list_display = ('movie', 'hall', 'start_time', 'price')
    list_filter = ('hall', 'movie')
    date_hierarchy = 'start_time'

from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['title', 'serial_number', 'restaurant', 'started_at', 'ended_at', 'is_archived']
    
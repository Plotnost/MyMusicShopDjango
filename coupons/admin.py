from django.contrib import admin
from .models import PercentageCoupon, FixedPriceCoupon


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']


admin.site.register(PercentageCoupon, CouponAdmin)
admin.site.register(FixedPriceCoupon, CouponAdmin)

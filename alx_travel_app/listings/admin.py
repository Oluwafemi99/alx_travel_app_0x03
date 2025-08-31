from django.contrib import admin
from .models import Payment


# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("booking_reference", "amount", "payment_status",
                    "transaction_id", "created_at")
    search_fields = ("booking_reference", "transaction_id", "payment_status")
    list_filter = ("payment_status", "created_at")

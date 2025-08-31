from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (BookingViews, ListingViews,
                    InitiatePaymentView, VerifyPaymentView)


router = DefaultRouter()
router.register(r'listings', ListingViews, basename='lising')
router.register(r'bookings', BookingViews, basename='booking')
path('api/', include(router.urls))

urlpatterns = [
    path('initiate_payment', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('verify_payment', VerifyPaymentView.as_view(), name='verify-payment'),
]

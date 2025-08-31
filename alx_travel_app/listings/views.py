from django.shortcuts import render
from rest_framework import viewsets
from .models import Booking, Listing
from .serializers import BookingSerializer, ListingSerializer
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from django.conf import settings
from .task import send_confirmation_email
import requests
import logging
from .tasks import send_booking_confirmation_email


# Create your views here.
class BookingViews(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        booking = serializer.save()
        # Trigger async email
        send_booking_confirmation_email.delay(booking.user.email, booking.id)


class ListingViews(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated]


class InitiatePaymentView(APIView):
    def post(self, request):
        booking_reference = request.data.get("booking_reference")
        amount = request.data.get("amount")
        email = request.data.get("email")

        payload = {
            "amount": str(amount),
            "currency": "NGN",
            "email": email,
            "tx_ref": booking_reference,
            "callback_url": "https://7e9b5c33d905.ngrok-free.app/api/verify-payment/",
            "return_url": "https://7e9b5c33d905.ngrok-free.app/payment-success/",
            "customization": {
                "title": "ALX Travel Booking",
                "description": "Payment for travel booking"
            }
        }

        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://api.chapa.co/v1/transaction/initialize",
            json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()["data"]
            Payment.objects.create(
                booking_reference=booking_reference,
                amount=amount,
                transaction_id=data["tx_ref"],
                status="Pending"
            )
            return Response({"checkout_url": data["checkout_url"]},
                            status=status.HTTP_200_OK)
        return Response(response.json(), status=response.status_code)


logger = logging.getLogger(__name__)


class VerifyPaymentView(APIView):
    def get(self, request):
        tx_ref = request.query_params.get("tx_ref")
        if not tx_ref:
            logger.warning("Missing tx_ref in verification request")
            return Response({"error": "Missing transaction reference"},
                            status=status.HTTP_400_BAD_REQUEST)

        url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
        headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json().get("data", {})
            status_value = data.get("status")

            payment = Payment.objects.filter(transaction_id=tx_ref).first()
            if not payment:
                logger.error(f"No payment found for tx_ref: {tx_ref}")
                return Response({"error": "Payment not found"},
                                status=status.HTTP_404_NOT_FOUND)

            payment.status = "Completed" if status_value == "success" else "Failed"
            payment.save()

            if status_value == "success":
                customer_email = data.get("customer", {}).get("email")
                if customer_email:
                    send_confirmation_email.delay(customer_email, tx_ref)

            logger.info(
                f"Payment {tx_ref} verified with status:{payment.status}")
            return Response({"status": payment.status},
                            status=status.HTTP_200_OK)

        except requests.RequestException as e:
            logger.exception(f"Error verifying payment with Chapa{e}")
            return Response({"error": "Verification failed"},
                            status=status.HTTP_502_BAD_GATEWAY)

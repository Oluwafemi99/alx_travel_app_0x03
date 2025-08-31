from alx_travel_app.alx_travel_app.celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_booking_confirmation_email(to_email, booking_details):
    subject = "Booking Confirmation"
    message = f"Dear customer,\n\nYour booking is confirmed:\n{booking_details}\n\nThank you!"
    send_mail(subject, message, 'noreply@travelapp.com', [to_email])

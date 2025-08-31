from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_booking_confirmation_email(user_email, booking_id):
    subject = "Booking Confirmation"
    message = f"Your booking (ID: {booking_id}) was successful!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)

    return f"Booking confirmation email sent to {user_email}"

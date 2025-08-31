from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_confirmation_email(booking_id, customer_email, listing_title):
    subject = 'Booking Confirmation'
    message = f"""
    Dear Customer,

    Your booking for "{listing_title}" has been confirmed!
    Booking ID: {booking_id}

    Thank you for choosing our service.

    Best regards,
    ALX Travel Team
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [customer_email]
    
    try:
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
    except Exception as e:
        # Log error (for debugging in production)
        print(f"Failed to send email for booking {booking_id}: {str(e)}")
        raise
from django.shortcuts import render
from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
import requests
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment, Booking
from celery import shared_task
from time import time

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


@shared_task
def send_payment_confirmation_email(user_email, booking_id, amount):
    subject = f'Payment Confirmation for Booking #{booking_id}'
    message = f'Your payment of {amount} for Booking #{booking_id} has been successfully processed.'
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [user_email])

class InitiatePaymentView(APIView):
    def post(self, request):
        # Assuming booking_id and amount are sent in the request
        booking_id = request.data.get('booking_id')
        amount = request.data.get('amount')
        user = request.user  # Assumes user is authenticated

        try:
            booking = Booking.objects.get(id=booking_id, user=user)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        # Generate a unique transaction reference
        tx_ref = f"TRAVEL-{booking_id}-{int(time.time())}"

        # Chapa API payload
        payload = {
            'amount': str(amount),
            'currency': 'ETB',  # Adjust based on your currency
            'email': user.email,
            'first_name': user.first_name or 'User',
            'last_name': user.last_name or 'User',
            'tx_ref': tx_ref,
            'callback_url': 'http://localhost:8000/api/payments/verify/',  # Update for production
            'return_url': 'http://localhost:8000/payment/success/'  # Update for production
        }

        headers = {
            'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        # Initiate payment with Chapa
        response = requests.post(
            'https://api.chapa.co/v1/transaction/initialize',
            json=payload,
            headers=headers
        )

        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('status') == 'success':
                # Create Payment record
                payment = Payment.objects.create(
                    booking=booking,
                    user=user,
                    amount=amount,
                    transaction_id=tx_ref,
                    status='PENDING'
                )
                return Response({
                    'message': 'Payment initiated successfully',
                    'payment_url': response_data['data']['checkout_url'],
                    'transaction_id': tx_ref
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to initiate payment'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Chapa API error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyPaymentView(APIView):
    def get(self, request):
        tx_ref = request.query_params.get('tx_ref')
        if not tx_ref:
            return Response({'error': 'Transaction ID required'}, status=status.HTTP_400_BAD_REQUEST)

        headers = {
            'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}'
        }

        # Verify payment with Chapa
        response = requests.get(
            f'https://api.chapa.co/v1/transaction/verify/{tx_ref}',
            headers=headers
        )

        try:
            payment = Payment.objects.get(transaction_id=tx_ref)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)

        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('status') == 'success':
                payment.status = 'COMPLETED'
                payment.save()
                # Send confirmation email via Celery
                send_payment_confirmation_email.delay(
                    payment.user.email,
                    payment.booking.id,
                    payment.amount
                )
                return Response({
                    'message': 'Payment verified successfully',
                    'status': payment.status
                }, status=status.HTTP_200_OK)
            else:
                payment.status = 'FAILED'
                payment.save()
                return Response({
                    'error': 'Payment verification failed',
                    'status': payment.status
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            payment.status = 'FAILED'
            payment.save()
            return Response({'error': 'Chapa API error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
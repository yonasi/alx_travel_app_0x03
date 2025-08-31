# ALX Travel App 0x03

A Django-based travel application with Celery and RabbitMQ for background task management and email notifications for booking confirmations.

<details>
<summary>Click to view full project documentation</summary>

## Project Overview

This project extends `alx_travel_app_0x02` by integrating Celery with RabbitMQ to handle asynchronous tasks, specifically sending booking confirmation emails when a booking is created via the REST API. The application uses Django REST Framework for API endpoints and Django’s email backend for notifications.

## Features

- **Asynchronous Email Notifications**: Sends booking confirmation emails using Celery when a booking is created.
- **REST API**: Manages bookings through the `BookingViewSet` at `/api/bookings/`.
- **Background Task Management**: Uses Celery with RabbitMQ as the message broker for reliable task execution.

## Prerequisites

- Python 3.8 or higher
- Django 4.2 or higher
- Celery 5.3 or higher
- RabbitMQ 3.8 or higher
- A valid SMTP email provider account (e.g., Gmail, SendGrid)
- Git for version control

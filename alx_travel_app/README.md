# ALX Travel App (alx_travel_app_0x02)

A Django-based travel booking app with Chapa API for payment processing.

## Setup

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd alx_travel_app_0x02

2. Set up a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

3. Configure environment variables in .env:
    ```text
    CHAPA_SECRET_KEY=CHAPA_AUTH_xxx

4. Apply migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate

5. Start Redis and Celery:
    ```bash
    redis-server
    celery -A alx_travel_app worker --loglevel=info

6. Run the server:
    ```bash
    python manage.py runserver
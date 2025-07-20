from django.core.management.base import BaseCommand
from listings.models import Listing
import random

class Command(BaseCommand):
    help = "Seed the database with sample listings"

    def handle(self, *args, **kwargs):
        sample_data = [
            {
                'title': 'Ocean View Apartment',
                'description': 'A beautiful apartment by the sea.',
                'location': 'Miami, FL',
                'price_per_night': 120.00,
                'available': True
            },
            {
                'title': 'Mountain Cabin Retreat',
                'description': 'Cozy cabin in the woods.',
                'location': 'Aspen, CO',
                'price_per_night': 200.00,
                'available': True
            },
            {
                'title': 'Urban Studio Loft',
                'description': 'Modern loft in downtown.',
                'location': 'New York, NY',
                'price_per_night': 150.00,
                'available': True
            }
        ]

        for data in sample_data:
            Listing.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Sample listings seeded successfully.'))
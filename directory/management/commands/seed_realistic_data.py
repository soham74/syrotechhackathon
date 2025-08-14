from django.core.management.base import BaseCommand
from scripts.seed_data import run

class Command(BaseCommand):
    help = 'Seed the database with realistic, diverse job postings'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting realistic data seeding...'))
        run()
        self.stdout.write(self.style.SUCCESS('Realistic data seeding completed successfully!'))

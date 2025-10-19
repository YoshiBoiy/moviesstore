from django.core.management.base import BaseCommand
from geographic.services import RegionService

class Command(BaseCommand):
    help = 'Populate the database with sample regions'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample regions...')
        RegionService.create_sample_regions()
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample regions')
        )

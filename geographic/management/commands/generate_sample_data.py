from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from movies.models import Movie
from geographic.models import Region, MoviePurchase, UserRegion
from geographic.services import TrendingCalculator
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Generate sample trending data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Generating sample trending data...')
        
        # Get or create a test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com'}
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write('Created test user: testuser / testpass123')
        
        # Get regions
        regions = Region.objects.all()
        if not regions.exists():
            self.stdout.write('No regions found. Run populate_regions first.')
            return
        
        # Get movies
        movies = Movie.objects.all()
        if not movies.exists():
            self.stdout.write('No movies found. Add some movies first.')
            return
        
        # Assign user to a random region
        user_region = random.choice(regions)
        UserRegion.objects.get_or_create(
            user=user,
            defaults={'region': user_region}
        )
        
        # Generate sample purchases for the last 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        # Clear existing sample data
        MoviePurchase.objects.filter(user=user).delete()
        
        # Generate random purchases
        for _ in range(20):  # Generate 20 random purchases
            movie = random.choice(movies)
            region = random.choice(regions)
            purchase_date = start_date + timedelta(
                seconds=random.randint(0, int((end_date - start_date).total_seconds()))
            )
            quantity = random.randint(1, 3)
            
            MoviePurchase.objects.create(
                movie=movie,
                user=user,
                region=region,
                purchase_date=purchase_date,
                quantity=quantity
            )
        
        # Update trending scores
        calculator = TrendingCalculator()
        calculator.update_trending_scores()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully generated sample trending data')
        )
        self.stdout.write(f'Created 20 sample purchases across {regions.count()} regions')
        self.stdout.write('Test user: testuser / testpass123')

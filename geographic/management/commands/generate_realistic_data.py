from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from movies.models import Movie
from geographic.models import Region, MoviePurchase, UserRegion
from geographic.services import TrendingCalculator
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Generate realistic trending data with regional preferences'

    def handle(self, *args, **options):
        self.stdout.write('Generating realistic trending data...')
        
        # Get or create test users
        users = []
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f'testuser{i+1}',
                defaults={'email': f'test{i+1}@example.com'}
            )
            if created:
                user.set_password('testpass123')
                user.save()
            users.append(user)
        
        # Get regions and movies
        regions = list(Region.objects.all())
        movies = list(Movie.objects.all())
        
        if not regions or not movies:
            self.stdout.write('No regions or movies found. Run populate_regions and add movies first.')
            return
        
        # Assign users to different regions
        for i, user in enumerate(users):
            region = regions[i % len(regions)]
            UserRegion.objects.get_or_create(
                user=user,
                defaults={'region': region}
            )
        
        # Clear existing sample data
        MoviePurchase.objects.all().delete()
        
        # Generate realistic purchase patterns
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)  # Last 30 days
        
        # Create regional preferences (some movies are more popular in certain regions)
        movie_count = len(movies)
        regional_preferences = {}
        for i, region in enumerate(regions):
            # Create preferences based on available movies
            if movie_count >= 3:
                regional_preferences[region.id] = list(range(min(3, movie_count)))
            else:
                regional_preferences[region.id] = list(range(movie_count))
        
        total_purchases = 0
        
        for day in range(30):
            current_date = start_date + timedelta(days=day)
            
            # Generate purchases for each region
            for region in regions:
                # Number of purchases per day varies by region size
                daily_purchases = random.randint(1, 5) + (region.population // 10000000)
                
                for _ in range(daily_purchases):
                    # Select user from this region
                    user_region = UserRegion.objects.filter(region=region).first()
                    if not user_region:
                        continue
                    
                    user = user_region.user
                    
                    # Select movie based on regional preferences
                    preferred_movies = regional_preferences.get(region.id, list(range(len(movies))))
                    if random.random() < 0.7 and preferred_movies:  # 70% chance to pick preferred movie
                        movie_index = random.choice(preferred_movies)
                        movie = movies[movie_index]
                    else:
                        movie = random.choice(movies)
                    
                    # Random time during the day
                    purchase_time = current_date + timedelta(
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59)
                    )
                    
                    quantity = random.randint(1, 3)
                    
                    MoviePurchase.objects.create(
                        movie=movie,
                        user=user,
                        region=region,
                        purchase_date=purchase_time,
                        quantity=quantity
                    )
                    total_purchases += 1
        
        # Update trending scores
        calculator = TrendingCalculator()
        calculator.update_trending_scores()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated {total_purchases} realistic purchases')
        )
        self.stdout.write('Test users: testuser1-5 / testpass123')
        self.stdout.write('Each user is assigned to a different region with regional movie preferences')

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from movies.models import Movie
from ratings.models import MovieRating
from ratings.services import RatingService
import random

class Command(BaseCommand):
    help = 'Generate sample ratings for testing'

    def handle(self, *args, **options):
        self.stdout.write('Generating sample ratings...')
        
        # Get or create test users
        users = []
        for i in range(10):
            user, created = User.objects.get_or_create(
                username=f'ratinguser{i+1}',
                defaults={'email': f'rating{i+1}@example.com'}
            )
            if created:
                user.set_password('testpass123')
                user.save()
            users.append(user)
        
        # Get movies
        movies = Movie.objects.all()
        if not movies.exists():
            self.stdout.write('No movies found. Add some movies first.')
            return
        
        # Clear existing sample ratings
        MovieRating.objects.filter(user__username__startswith='ratinguser').delete()
        
        # Generate random ratings
        total_ratings = 0
        for user in users:
            # Each user rates 3-7 random movies
            num_ratings = random.randint(3, 7)
            user_movies = random.sample(list(movies), min(num_ratings, len(movies)))
            
            for movie in user_movies:
                rating_value = random.randint(1, 5)
                MovieRating.objects.create(
                    user=user,
                    movie=movie,
                    rating=rating_value
                )
                total_ratings += 1
        
        # Update all rating aggregates
        RatingService.update_all_rating_aggregates()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated {total_ratings} sample ratings')
        )
        self.stdout.write('Test users: ratinguser1-10 / testpass123')

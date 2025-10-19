from django.core.management.base import BaseCommand
from movies.models import Movie
from ratings.services import RatingService

class Command(BaseCommand):
    help = 'Initialize rating aggregates for all movies'

    def handle(self, *args, **options):
        self.stdout.write('Initializing rating aggregates...')
        
        movies = Movie.objects.all()
        updated_count = 0
        
        for movie in movies:
            RatingService.update_movie_rating_aggregate(movie)
            updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully initialized rating aggregates for {updated_count} movies')
        )

from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from .models import Region, TrendingMovie, MoviePurchase, UserRegion
from movies.models import Movie

class TrendingCalculator:
    """Service class for calculating trending movies by region"""
    
    def __init__(self):
        self.trending_period_days = 7  # Calculate trending over last 7 days
    
    def calculate_trending_for_region(self, region_id, limit=10):
        """Calculate trending movies for a specific region"""
        region = Region.objects.get(id=region_id)
        period_start = timezone.now() - timedelta(days=self.trending_period_days)
        period_end = timezone.now()
        
        # Get purchase data for the region in the time period
        purchases = MoviePurchase.objects.filter(
            region=region,
            purchase_date__gte=period_start,
            purchase_date__lte=period_end
        )
        
        # Calculate trending scores for each movie
        movie_stats = {}
        for purchase in purchases:
            movie_id = purchase.movie.id
            if movie_id not in movie_stats:
                movie_stats[movie_id] = {
                    'movie': purchase.movie,
                    'purchase_count': 0,
                    'total_quantity': 0
                }
            movie_stats[movie_id]['purchase_count'] += 1
            movie_stats[movie_id]['total_quantity'] += purchase.quantity
        
        # Calculate trending score (purchase count * quantity * recency factor)
        trending_movies = []
        for movie_id, stats in movie_stats.items():
            # Simple trending score: purchase count * total quantity
            # In a real implementation, you might add recency weighting
            trending_score = stats['purchase_count'] * stats['total_quantity']
            
            trending_movies.append({
                'movie': stats['movie'],
                'purchase_count': stats['purchase_count'],
                'total_quantity': stats['total_quantity'],
                'trending_score': trending_score
            })
        
        # Sort by trending score and return top movies
        trending_movies.sort(key=lambda x: x['trending_score'], reverse=True)
        return trending_movies[:limit]
    
    def calculate_trending_for_all_regions(self):
        """Calculate trending movies for all active regions"""
        regions = Region.objects.filter(is_active=True)
        all_trending = {}
        
        for region in regions:
            trending = self.calculate_trending_for_region(region.id)
            all_trending[region.id] = {
                'region': region,
                'trending_movies': trending
            }
        
        return all_trending
    
    def update_trending_scores(self):
        """Update trending scores in the database"""
        period_start = timezone.now() - timedelta(days=self.trending_period_days)
        period_end = timezone.now()
        
        # Clear existing trending data for this period
        TrendingMovie.objects.filter(
            period_start=period_start,
            period_end=period_end
        ).delete()
        
        # Calculate and save new trending data
        all_trending = self.calculate_trending_for_all_regions()
        
        for region_id, data in all_trending.items():
            region = data['region']
            for movie_data in data['trending_movies']:
                TrendingMovie.objects.create(
                    movie=movie_data['movie'],
                    region=region,
                    purchase_count=movie_data['purchase_count'],
                    view_count=0,  # Could be implemented later
                    trending_score=movie_data['trending_score'],
                    period_start=period_start,
                    period_end=period_end
                )

class RegionService:
    """Service class for managing regions and user locations"""
    
    @staticmethod
    def get_user_region(user):
        """Get the region for a specific user"""
        try:
            user_region = UserRegion.objects.get(user=user)
            return user_region.region
        except UserRegion.DoesNotExist:
            return None
    
    @staticmethod
    def set_user_region(user, region):
        """Set the region for a specific user"""
        user_region, created = UserRegion.objects.get_or_create(
            user=user,
            defaults={'region': region}
        )
        if not created:
            user_region.region = region
            user_region.save()
        return user_region
    
    @staticmethod
    def create_sample_regions():
        """Create sample regions for testing"""
        sample_regions = [
            {'name': 'Georgia', 'code': 'US-GA', 'latitude': 33.7490, 'longitude': -84.3880, 'population': 10711908},
            {'name': 'California', 'code': 'US-CA', 'latitude': 36.7783, 'longitude': -119.4179, 'population': 39538223},
            {'name': 'New York', 'code': 'US-NY', 'latitude': 42.1657, 'longitude': -74.9481, 'population': 20201249},
            {'name': 'Texas', 'code': 'US-TX', 'latitude': 31.9686, 'longitude': -98.5350, 'population': 29145505},
            {'name': 'Florida', 'code': 'US-FL', 'latitude': 27.7663, 'longitude': -82.6404, 'population': 21538187},
        ]
        
        for region_data in sample_regions:
            Region.objects.get_or_create(
                code=region_data['code'],
                defaults=region_data
            )

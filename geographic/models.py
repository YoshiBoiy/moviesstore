from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie

class Region(models.Model):
    """Represents a geographic region for trending movie analysis"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)  # e.g., 'US-GA', 'US-CA'
    latitude = models.FloatField()
    longitude = models.FloatField()
    population = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class UserRegion(models.Model):
    """Links users to their geographic regions"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.region.name}"

class TrendingMovie(models.Model):
    """Tracks trending movies by region and time period"""
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    purchase_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    trending_score = models.FloatField(default=0.0)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['movie', 'region', 'period_start']
        ordering = ['-trending_score']
    
    def __str__(self):
        return f"{self.movie.name} in {self.region.name} - Score: {self.trending_score}"

class MoviePurchase(models.Model):
    """Tracks individual movie purchases for trending calculations"""
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.user.username} purchased {self.movie.name} in {self.region.name}"
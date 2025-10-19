from django.contrib import admin
from .models import Region, UserRegion, TrendingMovie, MoviePurchase

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'latitude', 'longitude', 'population', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code']

@admin.register(UserRegion)
class UserRegionAdmin(admin.ModelAdmin):
    list_display = ['user', 'region', 'updated_at']
    list_filter = ['region', 'updated_at']
    search_fields = ['user__username', 'region__name']

@admin.register(TrendingMovie)
class TrendingMovieAdmin(admin.ModelAdmin):
    list_display = ['movie', 'region', 'trending_score', 'purchase_count', 'view_count', 'period_start']
    list_filter = ['region', 'period_start', 'created_at']
    search_fields = ['movie__name', 'region__name']
    ordering = ['-trending_score']

@admin.register(MoviePurchase)
class MoviePurchaseAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user', 'region', 'purchase_date', 'quantity']
    list_filter = ['region', 'purchase_date', 'movie']
    search_fields = ['movie__name', 'user__username', 'region__name']
    ordering = ['-purchase_date']
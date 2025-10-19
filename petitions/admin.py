from django.contrib import admin
from .models import Petition, Vote

@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'movie_title', 'created_by', 'created_at', 'is_active', 'yes_votes_count', 'no_votes_count', 'total_votes_count']
    list_filter = ['is_active', 'created_at', 'movie_year']
    search_fields = ['title', 'movie_title', 'movie_director', 'description']
    readonly_fields = ['created_at', 'updated_at', 'yes_votes_count', 'no_votes_count', 'total_votes_count']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Petition Information', {
            'fields': ('title', 'description', 'is_active')
        }),
        ('Movie Information', {
            'fields': ('movie_title', 'movie_year', 'movie_director')
        }),
        ('User Information', {
            'fields': ('created_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Vote Statistics', {
            'fields': ('yes_votes_count', 'no_votes_count', 'total_votes_count'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'petition', 'vote_type', 'created_at']
    list_filter = ['vote_type', 'created_at']
    search_fields = ['user__username', 'petition__title', 'petition__movie_title']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'petition')
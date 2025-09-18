from django.contrib import admin
from .models import SecurityPhrase

@admin.register(SecurityPhrase)
class SecurityPhraseAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'question']
    readonly_fields = ['created_at', 'updated_at']

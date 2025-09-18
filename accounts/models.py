from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class SecurityPhrase(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='security_phrase')
    question = models.CharField(max_length=200, validators=[MinLengthValidator(10)])
    answer = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.question[:50]}..."
    
    class Meta:
        verbose_name = "Security Phrase"
        verbose_name_plural = "Security Phrases"

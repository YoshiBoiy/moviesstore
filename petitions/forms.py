from django import forms
from django.core.exceptions import ValidationError
from .models import Petition, Vote

class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['title', 'description', 'movie_title', 'movie_year', 'movie_director']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a descriptive title for your petition'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Explain why you think this movie should be added to the catalog...'
            }),
            'movie_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the exact movie title'
            }),
            'movie_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Year (optional)',
                'min': '1900',
                'max': '2030'
            }),
            'movie_director': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Director name (optional)'
            }),
        }
    
    def clean_movie_year(self):
        year = self.cleaned_data.get('movie_year')
        if year and (year < 1900 or year > 2030):
            raise ValidationError('Please enter a valid year between 1900 and 2030.')
        return year
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title.strip()) < 5:
            raise ValidationError('Title must be at least 5 characters long.')
        return title.strip()
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description.strip()) < 20:
            raise ValidationError('Description must be at least 20 characters long.')
        return description.strip()

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['vote_type']
        widgets = {
            'vote_type': forms.RadioSelect(choices=Vote.VOTE_CHOICES)
        }
    
    def __init__(self, *args, **kwargs):
        self.petition = kwargs.pop('petition', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        vote_type = cleaned_data.get('vote_type')
        
        if not vote_type:
            raise ValidationError('Please select a vote option.')
        
        # Check if user has already voted
        if self.user and self.petition and self.petition.has_user_voted(self.user):
            raise ValidationError('You have already voted on this petition.')
        
        return cleaned_data
    
    def save(self, commit=True):
        vote = super().save(commit=False)
        vote.petition = self.petition
        vote.user = self.user
        if commit:
            vote.save()
        return vote


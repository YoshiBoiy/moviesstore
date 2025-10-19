from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import Petition, Vote
from .forms import PetitionForm, VoteForm

def petition_list(request):
    """Display all active petitions"""
    template_data = {}
    template_data['title'] = 'Movie Petitions'
    
    # Get search query
    search_query = request.GET.get('search', '')
    
    # Filter petitions
    petitions = Petition.objects.filter(is_active=True)
    
    if search_query:
        petitions = petitions.filter(
            Q(title__icontains=search_query) |
            Q(movie_title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(movie_director__icontains=search_query)
        )
    
    # Add vote counts and user vote status
    for petition in petitions:
        petition.yes_count = petition.yes_votes_count
        petition.no_count = petition.no_votes_count
        petition.total_count = petition.total_votes_count
        petition.user_vote = petition.get_user_vote(request.user) if request.user.is_authenticated else None
    
    template_data['petitions'] = petitions
    template_data['search_query'] = search_query
    
    return render(request, 'petitions/index.html', {'template_data': template_data})

def petition_detail(request, petition_id):
    """Display petition details and voting form"""
    template_data = {}
    petition = get_object_or_404(Petition, id=petition_id, is_active=True)
    template_data['title'] = f'Petition: {petition.title}'
    template_data['petition'] = petition
    
    # Add vote counts
    petition.yes_count = petition.yes_votes_count
    petition.no_count = petition.no_votes_count
    petition.total_count = petition.total_votes_count
    petition.user_vote = petition.get_user_vote(request.user) if request.user.is_authenticated else None
    
    # Handle voting
    if request.user.is_authenticated and not petition.has_user_voted(request.user):
        if request.method == 'POST':
            vote_form = VoteForm(request.POST, petition=petition, user=request.user)
            if vote_form.is_valid():
                vote_form.save()
                messages.success(request, 'Your vote has been recorded!')
                return redirect('petitions.detail', petition_id=petition.id)
        else:
            vote_form = VoteForm(petition=petition, user=request.user)
    else:
        vote_form = None
    
    template_data['vote_form'] = vote_form
    template_data['can_vote'] = request.user.is_authenticated and not petition.has_user_voted(request.user)
    
    return render(request, 'petitions/detail.html', {'template_data': template_data})

@login_required
def petition_create(request):
    """Create a new petition"""
    template_data = {}
    template_data['title'] = 'Create Movie Petition'
    
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            messages.success(request, 'Your petition has been created successfully!')
            return redirect('petitions.detail', petition_id=petition.id)
    else:
        form = PetitionForm()
    
    template_data['form'] = form
    return render(request, 'petitions/create.html', {'template_data': template_data})

@login_required
@require_http_methods(["POST"])
def petition_vote(request, petition_id):
    """Handle AJAX voting"""
    petition = get_object_or_404(Petition, id=petition_id, is_active=True)
    
    if petition.has_user_voted(request.user):
        return JsonResponse({
            'success': False,
            'message': 'You have already voted on this petition.'
        })
    
    vote_type = request.POST.get('vote_type')
    if vote_type not in ['yes', 'no']:
        return JsonResponse({
            'success': False,
            'message': 'Invalid vote type.'
        })
    
    # Create the vote
    Vote.objects.create(
        petition=petition,
        user=request.user,
        vote_type=vote_type
    )
    
    # Return updated counts
    return JsonResponse({
        'success': True,
        'message': 'Your vote has been recorded!',
        'yes_count': petition.yes_votes_count,
        'no_count': petition.no_votes_count,
        'total_count': petition.total_votes_count
    })

@login_required
def my_petitions(request):
    """Display user's own petitions"""
    template_data = {}
    template_data['title'] = 'My Petitions'
    
    petitions = Petition.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Add vote counts
    for petition in petitions:
        petition.yes_count = petition.yes_votes_count
        petition.no_count = petition.no_votes_count
        petition.total_count = petition.total_votes_count
    
    template_data['petitions'] = petitions
    return render(request, 'petitions/my_petitions.html', {'template_data': template_data})
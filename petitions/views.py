from django.shortcuts import render

def petition_list(request):
    """Display all active petitions"""
    template_data = {}
    template_data['title'] = 'Movie Petitions'
    template_data['petitions'] = []
    template_data['search_query'] = ''
    
    return render(request, 'petitions/index.html', {'template_data': template_data})

def petition_detail(request, petition_id):
    """Display petition details and voting form"""
    template_data = {}
    template_data['title'] = 'Petition Details'
    template_data['petition'] = None
    template_data['vote_form'] = None
    template_data['can_vote'] = False
    
    return render(request, 'petitions/detail.html', {'template_data': template_data})

def petition_create(request):
    """Create a new petition"""
    template_data = {}
    template_data['title'] = 'Create Movie Petition'
    template_data['form'] = None
    
    return render(request, 'petitions/create.html', {'template_data': template_data})

def my_petitions(request):
    """Display user's own petitions"""
    template_data = {}
    template_data['title'] = 'My Petitions'
    template_data['petitions'] = []
    
    return render(request, 'petitions/my_petitions.html', {'template_data': template_data})
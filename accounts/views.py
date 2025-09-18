from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from .forms import CustomUserCreationForm, CustomErrorList, SecurityPhraseForm, ForgotPasswordForm, PasswordResetForm
from .models import SecurityPhrase

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'

    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html', {'template_data': template_data})

@login_required
def settings(request):
    template_data = {}
    template_data['title'] = 'Account Settings'
    
    # Get or create security phrase for the user
    security_phrase, created = SecurityPhrase.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = SecurityPhraseForm(request.POST, instance=security_phrase)
        if form.is_valid():
            form.save()
            messages.success(request, 'Security phrase updated successfully!')
            return redirect('accounts.settings')
        else:
            template_data['form'] = form
    else:
        template_data['form'] = SecurityPhraseForm(instance=security_phrase)
    
    template_data['security_phrase'] = security_phrase
    return render(request, 'accounts/settings.html', {'template_data': template_data})

def forgot_password(request):
    template_data = {}
    template_data['title'] = 'Forgot Password'
    
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
                if hasattr(user, 'security_phrase'):
                    # Store username in session for password reset
                    request.session['reset_username'] = username
                    return redirect('accounts.security_question')
                else:
                    messages.error(request, 'No security phrase found for this account. Please contact support.')
            except User.DoesNotExist:
                messages.error(request, 'Username not found.')
        else:
            template_data['form'] = form
    else:
        template_data['form'] = ForgotPasswordForm()
    
    return render(request, 'accounts/forgot_password.html', {'template_data': template_data})

def security_question(request):
    template_data = {}
    template_data['title'] = 'Security Question'
    
    username = request.session.get('reset_username')
    if not username:
        return redirect('accounts.forgot_password')
    
    try:
        user = User.objects.get(username=username)
        security_phrase = user.security_phrase
        template_data['question'] = security_phrase.question
    except (User.DoesNotExist, SecurityPhrase.DoesNotExist):
        messages.error(request, 'Invalid request.')
        return redirect('accounts.forgot_password')
    
    if request.method == 'POST':
        answer = request.POST.get('answer', '').strip().lower()
        if answer == security_phrase.answer.lower():
            # Store verification in session
            request.session['security_verified'] = True
            return redirect('accounts.reset_password')
        else:
            messages.error(request, 'Incorrect answer. Please try again.')
    
    return render(request, 'accounts/security_question.html', {'template_data': template_data})

def reset_password(request):
    template_data = {}
    template_data['title'] = 'Reset Password'
    
    username = request.session.get('reset_username')
    verified = request.session.get('security_verified')
    
    if not username or not verified:
        return redirect('accounts.forgot_password')
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, 'Invalid request.')
        return redirect('accounts.forgot_password')
    
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            
            # Clear session data
            request.session.pop('reset_username', None)
            request.session.pop('security_verified', None)
            
            messages.success(request, 'Password reset successfully! You can now login with your new password.')
            return redirect('accounts.login')
        else:
            template_data['form'] = form
    else:
        template_data['form'] = PasswordResetForm()
    
    return render(request, 'accounts/reset_password.html', {'template_data': template_data})
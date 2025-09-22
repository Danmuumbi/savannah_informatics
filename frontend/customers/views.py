

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlencode
import requests
from .models import EmailVerificationToken  # Import your model

def manual_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        
        print(f"Attempting login with email: {email}, name: {name}")
        
        # Check if customer exists in backend
        try:
            response = requests.get(
                # 'http://localhost:8000/api/customer/check/',
                'https://savannah-informatics-assignment.onrender.com/api/customer/check/',
                params={'email': email, 'name': name},
                timeout=5
            )
            
            print(f"Backend API response: {response.status_code}, {response.json()}")
            
            if response.status_code == 200 and response.json().get('exists'):
                # Create or get user for frontend session
                user, created = User.objects.get_or_create(
                    username=email,
                    defaults={
                        'email': email, 
                        'first_name': name,
                        'is_active': True
                    }
                )
                
                if created:
                    user.set_unusable_password()
                    user.save()
                    print(f"Created new user: {user}")
                else:
                    print(f"Found existing user: {user}")
                
                # Create verification token
                token = EmailVerificationToken.objects.create(user=user)
                
                # Build verification URL
                verification_url = request.build_absolute_uri(
                    reverse('verify_email') + '?' + urlencode({'token': token.token})
                )
                
                # Send verification email
                send_mail(
                    'Verify Your Login - Savannah Informatics',
                    f'Hello {name},\n\nPlease click the following link to verify your login and access your dashboard:\n\n{verification_url}\n\nThis link will expire in 24 hours.\n\nIf you did not request this login, please ignore this email.',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                
                # Store user ID in session for verification
                request.session['verification_user_id'] = user.id
                request.session['verification_pending'] = True
                
                messages.success(request, 'Please check your email for a verification link to complete your login.')
                print("Verification email sent, redirecting to pending page")
                return redirect('verification_pending')
            else:
                error_msg = 'No customer found with these details. Please contact administrator.'
                messages.error(request, error_msg)
                print(error_msg)
                
        except requests.RequestException as e:
            error_msg = 'Cannot connect to server. Please try again later.'
            messages.error(request, error_msg)
            print(f"Request error: {e}")
    
    return render(request, 'manual_login.html')

def verify_email(request):
    token_value = request.GET.get('token')
    
    if not token_value:
        messages.error(request, 'Invalid verification link.')
        return redirect('manual_login')
    
    try:
        token = EmailVerificationToken.objects.get(token=token_value, is_used=False)
        
        if token.is_expired():
            messages.error(request, 'Verification link has expired. Please log in again.')
            return redirect('manual_login')
        
        # Mark token as used
        token.is_used = True
        token.save()
        
        # Log the user in
        user = token.user
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        
        # Clear verification session data
        if 'verification_user_id' in request.session:
            del request.session['verification_user_id']
        if 'verification_pending' in request.session:
            del request.session['verification_pending']
        
        messages.success(request, 'Email verified successfully. Welcome to your dashboard!')
        return redirect('dashboard')
        
    except EmailVerificationToken.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('manual_login')

def verification_pending(request):
    if not request.session.get('verification_pending'):
        return redirect('manual_login')
    
    return render(request, 'verification_pending.html')

def dashboard(request):
    if not request.user.is_authenticated:
        print("User not authenticated, redirecting to login")
        return redirect('manual_login')
    
    print(f"User {request.user.email} authenticated, loading dashboard")
    
    try:
        # Get customer orders from backend
        response = requests.get(
            # 'http://localhost:8000/api/customer/orders/',
            'https://savannah-informatics-assignment.onrender.com/api/customer/orders/',
            params={'email': request.user.email},
            timeout=5
        )
        
        print(f"Orders API response status: {response.status_code}")
        print(f"Orders API response content: {response.text}")
        
        if response.status_code == 200:
            orders = response.json()
            print(f"Successfully fetched {len(orders)} orders")
        else:
            orders = []
            print(f"Failed to fetch orders. Status: {response.status_code}")
            messages.error(request, 'Could not fetch orders. Please try again.')
            
    except requests.RequestException as e:
        orders = []
        print(f"Request error: {e}")
        messages.error(request, 'Cannot connect to server. Please try again later.')
    
    return render(request, 'dashboard.html', {
        'user': request.user,
        'orders': orders
    })



def resend_verification(request):
    if not request.session.get('verification_user_id'):
        return redirect('manual_login')
    
    user_id = request.session['verification_user_id']
    user = get_object_or_404(User, id=user_id)
    
    # Invalidate previous tokens
    EmailVerificationToken.objects.filter(user=user, is_used=False).update(is_used=True)
    
    # Create new verification token
    token = EmailVerificationToken.objects.create(user=user)
    
    # Build verification URL
    verification_url = request.build_absolute_uri(
        reverse('verify_email') + '?' + urlencode({'token': token.token})
    )
    
    # Send verification email
    send_mail(
        'Verify Your Login - Savannah Informatics',
        f'Hello {user.first_name},\n\nPlease click the following link to verify your login and access your dashboard:\n\n{verification_url}\n\nThis link will expire in 24 hours.\n\nIf you did not request this login, please ignore this email.',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    
    messages.success(request, 'A new verification email has been sent.')
    return redirect('verification_pending')
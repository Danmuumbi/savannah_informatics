from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
import requests

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """Check if social login user exists in our backend"""
        email = sociallogin.user.email
        name = sociallogin.user.get_full_name() or sociallogin.user.username
        
        # Check if customer exists in backend
        try:
            response = requests.get(
                'http://localhost:8000/api/customers/check/',
                params={'email': email, 'name': name},
                timeout=5
            )
            
            if not (response.status_code == 200 and response.json().get('exists')):
                # Customer doesn't exist in backend, prevent login
                from django.core.exceptions import PermissionDenied
                raise PermissionDenied("No customer account found. Please contact administrator.")
                
        except requests.RequestException:
          
            pass

SOCIALACCOUNT_ADAPTER = 'customers.adapters.CustomSocialAccountAdapter'
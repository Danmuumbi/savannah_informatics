from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
import requests


API_BACKEND_URL = 'https://savannah-informatics-assignment.onrender.com'

class EmailNameBackend(ModelBackend):
    """Authenticate using only email and name (no password)"""
    
    def authenticate(self, request, email=None, name=None, **kwargs):
        try:
            # Check if customer exists in backend via API
            response = requests.get(

                   f'{API_BACKEND_URL}/api/customers/check/',
                params={'email': email, 'name': name}
                )
            #     f'http://localhost:8000/api/customers/check/',
            #     params={'email': email, 'name': name}
            # )
            
            if response.status_code == 200:
                # Create or get user
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={'username': email, 'first_name': name}
                )
                if created:
                    user.set_unusable_password()  # No password needed
                    user.save()
                return user
                
        except requests.RequestException:
            pass
        return None
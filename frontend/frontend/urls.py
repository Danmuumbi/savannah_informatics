from django.urls import path, include
from django.views.generic import RedirectView
from customers import views

urlpatterns = [
    # Home page - manual login
    path('', views.manual_login, name='manual_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Redirect allauth URLs to our manual login
    path('accounts/', include([
        path('login/', RedirectView.as_view(url='/', permanent=False), name='account_login'),
        path('signup/', RedirectView.as_view(url='/', permanent=False), name='account_signup'),
        path('', include('allauth.urls')),  



             path('verify-email/', views.verify_email, name='verify_email'),
    path('verification-pending/', views.verification_pending, name='verification_pending'),
    path('resend-verification/', views.resend_verification, name='resend_verification'),
    path('dashboard/', views.dashboard, name='dashboard'),
    ])),
]
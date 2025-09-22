from django.db import models
from django.conf import settings

# This model maps to the existing backend customers table
class Customer(models.Model):
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False  
        db_table = 'customers_customer'  

    def __str__(self):
        return self.name
    



import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class EmailVerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    def is_expired(self):
        return (timezone.now() - self.created_at).days > 1  
        
    def __str__(self):
        return f"{self.user.email} - {self.token} - {'Used' if self.is_used else 'Active'}"









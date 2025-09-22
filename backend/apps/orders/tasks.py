from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
import requests

@shared_task
def send_order_sms(order_id):
    from apps.orders.models import Order
    
    try:
        order = Order.objects.get(id=order_id)
        
        message = f"Hello {order.customer.name}, your order #{order.id} has been received. "
        message += f"Total: KES {order.total_amount}. Thank you for shopping with us!"
        
        # Use Africa's Talking API directly (working approach from test)
        url = "https://api.sandbox.africastalking.com/version1/messaging"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "apiKey": settings.AFRICASTALKING_API_KEY
        }
        
        data = {
            "username": settings.AFRICASTALKING_USERNAME,
            "to": order.customer.phone_number,
            "message": message,
            "from": "E-commerce"  # Using the working sender ID from your test
        }
        
        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 201:
            return f"SMS sent to {order.customer.phone_number}: {response.json()}"
        else:
            return f"SMS failed: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"Failed to send SMS: {str(e)}"

@shared_task
def send_admin_email(order_id):
    from apps.orders.models import Order
    
    try:
        order = Order.objects.get(id=order_id)
        
        subject = f"New Order Received - #{order.id}"
        
        context = {
            'order': order,
            'items': order.items.all()
        }
        
        message = render_to_string('emails/order_notification.txt', context)
        html_message = render_to_string('emails/order_notification.html', context)
        
      
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
        
        return f"Email sent to admin for order #{order.id}"
    
    except Exception as e:
        return f"Failed to send email: {str(e)}"
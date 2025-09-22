import logging
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import africastalking
import redis

logger = logging.getLogger(__name__)

def is_redis_available():
    """Check if Redis is available"""
    try:
        r = redis.Redis(host='redis', port=6379, db=0)
        r.ping()
        return True
    except (redis.ConnectionError, redis.TimeoutError):
        return False

def send_order_notifications(order):
    """Send order notifications with fallback mechanism"""
   
    if is_redis_available():
        try:
            from .tasks import send_order_sms, send_admin_email
            send_order_sms.delay(order.id)
            send_admin_email.delay(order.id)
            return True, "Notifications sent via Celery"
        except Exception as e:
            logger.error(f"Celery task failed: {str(e)}")
            
            return send_notifications_fallback(order)
    else:
      
        return send_notifications_fallback(order)

def send_notifications_fallback(order):
    """Fallback method to send notifications without Celery"""
    try:
        # Send SMS
        sms_success = send_sms_direct(
            order.customer.phone_number,
            f"Hello {order.customer.name}, your order #{order.id} has been received. "
            f"Total: KES {order.total_amount}. Thank you for shopping with us!"
        )
        
        # Send email
        email_success = send_email_direct(
            f"New Order Received - #{order.id}",
            render_to_string('emails/order_notification.txt', {
                'order': order,
                'items': order.items.all()
            }),
            [settings.ADMIN_EMAIL],
            render_to_string('emails/order_notification.html', {
                'order': order,
                'items': order.items.all()
            })
        )
        
        if sms_success and email_success:
            return True, "Notifications sent via fallback method"
        else:
            return False, f"Some notifications failed. SMS: {sms_success}, Email: {email_success}"
            
    except Exception as e:
        logger.error(f"Fallback notification failed: {str(e)}")
        return False, f"All notification methods failed: {str(e)}"

def send_sms_direct(phone_number, message):
    """Send SMS directly without Celery"""
    try:
        africastalking.initialize(
            username=settings.AFRICASTALKING_USERNAME,
            api_key=settings.AFRICASTALKING_API_KEY
        )
        sms = africastalking.SMS
        response = sms.send(message, [phone_number])
        return True
    except Exception as e:
        logger.error(f"SMS sending failed: {str(e)}")
        return False

def send_email_direct(subject, message, recipient_list, html_message=None):
    """Send email directly without Celery"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.error(f"Email sending failed: {str(e)}")
        return False
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny  
from .models import Customer
from ..orders.models import Order

@api_view(['GET'])
@permission_classes([AllowAny]) 
def check_customer(request):
    """Check if customer exists by email and name"""
    email = request.GET.get('email')
    name = request.GET.get('name')
    
    print(f"Checking customer: email={email}, name={name}")
    
    try:
        customer = Customer.objects.get(email=email, name=name)
        print(f"Customer found: {customer}")
        return Response({'exists': True, 'customer_id': customer.id})
    except Customer.DoesNotExist:
        print("Customer not found")
        return Response({'exists': False}, status=404)

@api_view(['GET'])
@permission_classes([AllowAny])  
def customer_orders(request):
    """Get orders for a customer by email"""
    email = request.GET.get('email')
    
    print(f"Fetching orders for email: {email}")
    
    try:
        # Find customer by email
        customer = Customer.objects.get(email=email)
        print(f"Found customer: {customer.name}")
        
        # Get orders for this customer
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        print(f"Found {orders.count()} orders for {customer.name}")
        
        # Serialize the orders
        orders_data = []
        for order in orders:
            orders_data.append({
                'id': order.id,
                'customer': order.customer.name,
                'order_date': order.order_date.strftime('%Y-%m-%d %H:%M:%S'),
                'status': order.status,
                'total_amount': str(order.total_amount),
                'notes': order.notes or '',
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return Response(orders_data)
        
    except Customer.DoesNotExist:
        print(f"No customer found with email: {email}")
        return Response([], status=404)
    except Exception as e:
        print(f"Error fetching orders: {e}")
        return Response([], status=500)
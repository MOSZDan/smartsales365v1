from django.urls import path

app_name = 'orders'

urlpatterns = [
    # Order endpoints will be added here
    # GET /api/orders/ - List user orders
    # POST /api/orders/ - Create order (checkout)
    # GET /api/orders/{id}/ - Order detail
    # PUT /api/orders/{id}/ - Update order status (seller/admin)
]

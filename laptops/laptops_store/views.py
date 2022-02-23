import datetime

from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Customer, Order, OrderItem, Laptop


@api_view(['POST'])
def orders(request):
    if request.method == 'POST':

        # with transaction.atomic():
        customer = request.data['customer']
        new_cust = Customer(name=customer['name'], address=customer['address'])
        new_cust.save()

        total_price = 0
        new_order = Order(customer=new_cust,
                          order_date=datetime.date.today(),
                          )
        new_order.save()

        items = request.data['items']
        for item in items:
            laptop = Laptop.objects.get(id=item['laptop_id'])
            total_price += laptop.price_euro

            oi = OrderItem(order=new_order,
                           laptop_id=item['laptop_id'],
                           item_price_euro=laptop.price_euro,
                           amnt=item['amount'])
            oi.save()

        new_order.total_price = total_price
        new_order.save()

        return Response(status=status.HTTP_201_CREATED)




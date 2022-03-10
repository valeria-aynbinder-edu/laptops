import datetime

from django.db import transaction, IntegrityError
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .custom_queries import total_stats_query, best_customers_query
from .models import Customer, Order, OrderItem, Laptop



from .serializers import NewOrderSerializer, LaptopSerializer


# @api_view(['GET'])
# def laptops(request):
#     if request.method == 'GET':
#         laptops = Laptop.objects.all()
#         ser = LaptopSerializer(laptops, many=True)
#         return Response(ser.data)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class LaptopsView(generics.ListAPIView):
    queryset = Laptop.objects.all()
    serializer_class = LaptopSerializer
    pagination_class = StandardResultsSetPagination

# Solution without serializers (totally ok, just requires more validation)
@api_view(['POST'])
def orders(request):
    # get authenticated user
    # user_id = request.user.id
    if request.method == 'POST':
        try:
            with transaction.atomic():
                customer = request.data['customer']
                new_cust = Customer(name=customer['name'], address=customer['address'])
                new_cust.save()


                new_order = Order(customer=new_cust,
                                  # customer_id=new_cust.id,
                                  order_date=datetime.date.today(),
                                  )
                new_order.save()

                items = request.data['items']
                total_price = 0
                for item in items:
                    laptop = Laptop.objects.get(id=item['laptop'])
                    total_price += laptop.price_euro * item['amnt']

                    oi = OrderItem(order=new_order,
                                   laptop_id=item['laptop'],
                                   item_price_euro=laptop.price_euro,
                                   amnt=item['amnt'])
                    oi.save()

                new_order.total_price = total_price
                new_order.save()

        except IntegrityError as error:
            print(f"Integrity error occurred during orders POST: {error}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_201_CREATED)


# Version 2 - Solution using serializers
@api_view(['POST'])
def orders_v2(request):
    if request.method == 'POST':
        serializer = NewOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def total_stats(request):
    stats_result = total_stats_query()
    print(stats_result)
    return Response(stats_result, status=status.HTTP_200_OK)


@api_view(['GET'])
def best_customers(request):
    from_date = request.GET.get('from_date', '1900-01-01')
    to_date = request.GET.get('to_date', str(datetime.date.today()))
    count = request.GET.get('count', 10)
    result = best_customers_query(from_date, to_date, count)
    print(result)
    return Response(result, status=status.HTTP_200_OK)




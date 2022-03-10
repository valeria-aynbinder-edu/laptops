import datetime

from django.db import transaction
from rest_framework import serializers, request
from rest_framework.fields import CharField

from .models import Laptop, OrderItem, Customer, Order


class LaptopSerializer(serializers.ModelSerializer):
    class Meta:
        model=Laptop
        fields = "__all__"


class NewOrderItemSerializer(serializers.Serializer):
    laptop = serializers.PrimaryKeyRelatedField(many=False, queryset=Laptop.objects.all())
    amnt = serializers.IntegerField()


class CustomerSerializer(serializers.Serializer):
    name = CharField(required=True, max_length=128)
    address = CharField(required=True, max_length=128)


class NewOrderSerializer(serializers.Serializer):
    customer = CustomerSerializer()
    items = NewOrderItemSerializer(many=True)


    def create(self, validated_data):
        with transaction.atomic():
            customer_data = validated_data.pop('customer')
            new_cust = Customer(**customer_data)
            new_cust.save()

            new_order = Order(customer=new_cust,
                              order_date=datetime.date.today(),
                              )
            new_order.save()

            items = validated_data['items']
            total_price = 0
            for item in items:
                laptop = item['laptop']
                total_price += laptop.price_euro * item['amnt']

                oi = OrderItem(order=new_order,
                               laptop=laptop,
                               item_price_euro=laptop.price_euro,
                               amnt=item['amnt'])
                oi.save()

        return new_order

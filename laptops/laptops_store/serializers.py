from rest_framework import serializers
from rest_framework.fields import CharField

from laptops.laptops_store.models import Laptop


class LaptopSerializer(serializers.ModelSerializer):
    class Meta:
        model=Laptop


class CustomerSerializer(serializers.Serializer):
    name = CharField(required=True, max_length=128)
    address = CharField(required=True, max_length=128)

class NewOrderSerializer(serializers.Serializer):
    customer = CustomerSerializer()
    # items = serializers.ListSerializer()

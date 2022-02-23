from django.db import models


class Manufacturer(models.Model):

    name = models.CharField(null=False, blank=False, max_length=64)

    class Meta:
        db_table = "manufacturers"


class Laptop(models.Model):

    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT)
    product_name = models.CharField(null=False, blank=False, max_length=256)
    type_name = models.CharField(null=False, blank=False, max_length=256)
    inches = models.FloatField(null=False, blank=False)
    resolution_w = models.PositiveIntegerField(null=False, blank=False)
    resolution_h = models.PositiveIntegerField(null=False, blank=False)
    cpu = models.CharField(null=False, blank=False, max_length=256)
    ram_gb = models.PositiveIntegerField(null=False, blank=False)
    mem_ssd_gb = models.PositiveIntegerField(null=True, blank=True)
    mem_hdd_gb = models.PositiveIntegerField(null=True, blank=True)
    mem_flash_gb = models.PositiveIntegerField(null=True, blank=True)
    mem_hybrid_gb = models.PositiveIntegerField(null=True, blank=True)
    gpu = models.CharField(null=False, blank=False, max_length=256)
    os = models.CharField(null=True, blank=True, max_length=128)
    weight_kg = models.FloatField(null=False, blank=False)
    price_euro = models.FloatField(null=False, blank=False)
    stock_amnt = models.PositiveIntegerField(null=False, blank=False)
    is_deleted = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        db_table = "laptops"


class Customer(models.Model):
    name = models.CharField(null=False, blank=False, max_length=256)
    address = models.CharField(null=False, blank=False, max_length=256)

    class Meta:
        db_table = "customers"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    order_date = models.DateField(auto_now_add=True)
    is_cancelled = models.BooleanField(null=False, blank=False, default=False)
    order_laptops = models.ManyToManyField(to=Laptop, through="OrderItem")
    total_price = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "orders"


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    laptop = models.ForeignKey(Laptop, on_delete=models.PROTECT)
    item_price_euro = models.FloatField(null=False, blank=False)
    amnt = models.PositiveIntegerField(null=False, blank=False)

    class Meta:
        db_table = "order_items"



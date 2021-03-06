# Generated by Django 3.2.12 on 2022-02-23 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laptops_store', '0002_auto_20220223_0927'),
    ]

    operations = [
        migrations.RenameField(
            model_name='laptop',
            old_name='manufacturer_id',
            new_name='manufacturer',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='customer_id',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='laptop_id',
            new_name='laptop',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='order_id',
            new_name='order',
        ),
    ]

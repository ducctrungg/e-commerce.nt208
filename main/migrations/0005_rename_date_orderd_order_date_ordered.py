# Generated by Django 4.2.7 on 2023-12-18 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_customer_phone_order_address_product_slug_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='date_orderd',
            new_name='date_ordered',
        ),
    ]

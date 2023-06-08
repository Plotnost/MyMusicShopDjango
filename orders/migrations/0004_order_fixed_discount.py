# Generated by Django 4.2.1 on 2023-06-08 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_rename_discount_order_percent_discount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='fixed_discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.code


class FixedPriceCoupon(Coupon):
    discount = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_discounted_price(self, price):
        return price - self.discount


class PercentageCoupon(Coupon):
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def calculate_discounted_price(self, price):
        discount_amount = (self.discount / 100) * price
        return price - discount_amount

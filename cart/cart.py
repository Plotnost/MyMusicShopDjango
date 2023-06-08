from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import FixedPriceCoupon, PercentageCoupon


class Cart(object):
    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохраняем пустую корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.percentage_coupon_id = self.session.get('percentage_coupon_id')
        self.fixed_coupon_ids = self.session.get('fixed_coupon_ids')

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    @property
    def percentage_coupon(self):
        if self.percentage_coupon_id:
            return PercentageCoupon.objects.get(id=self.percentage_coupon_id)
        return None

    def fixed_coupon(self):
        if self.fixed_coupon_ids:
            return FixedPriceCoupon.objects.filter(id__in=self.fixed_coupon_ids)
        return None

    def get_fixed_discount(self):
        discount = 0
        if self.fixed_coupon():
            for coupon in self.fixed_coupon():
                discount += coupon.discount
        return discount

    def get_discount(self):
        discount = Decimal('0')
        if self.percentage_coupon:
            discount += (self.percentage_coupon.discount / Decimal('100')) * self.get_total_price()
        if self.fixed_coupon():
            for coupon in self.fixed_coupon():
                discount += coupon.discount
        return discount

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()

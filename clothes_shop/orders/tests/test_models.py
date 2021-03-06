from datetime import datetime, timedelta

from django.test import TestCase

from shop.models import Category, Product
from coupons.models import Coupon

from ..models import Order, OrderItem


class BaseModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(BaseModelTestCase, cls).setUpClass()
        coupon = Coupon(
            code='sale', valid_from=datetime.now(), discount=10, active=True,
            valid_to=datetime.now()+timedelta(days=10)
        )
        coupon.save()
        cls.order_sale = Order(
            first_name='Имя', last_name='Фамилия', email='mail@mail.mail',
            address='Улица, дом 1', postal_code='123', city='Город',
            discount=10, coupon=coupon
        )
        cls.order_sale.save()
        cls.order = Order(
            first_name='Имя', last_name='Фамилия', email='mail@mail.mail',
            address='Улица, дом 1', postal_code='123', city='Город'
        )
        cls.order.save()
        category = Category(name='category_name', slug='category_slug')
        category.save()
        product_1 = Product(
            category=category, name='product_1', slug='slug_1', price=5, stock=1
        )
        product_2 = Product(
            category=category, name='product_2', slug='slug_2', price=5, stock=1
        )
        product_1.save()
        product_2.save()
        cls.order_item_1 = OrderItem(
            order=cls.order, product=product_1, price=product_1.price,
        )
        cls.order_item_2 = OrderItem(
            order=cls.order, product=product_2, price=product_2.price,
            quantity=5
        )
        cls.order_item_1.save()
        cls.order_item_2.save()
        cls.order_sale_item = OrderItem(
            order=cls.order_sale, product=product_2, price=product_2.price,
            quantity=5
        )
        cls.order_sale_item.save()


class OrderModelTest(BaseModelTestCase):
    """
    Тесты модели заказа товаров
    """
    def test_order_contain_two_items(self):
        self.assertEqual(len(self.order.items.all()), 2,
                         'Order does not contain two item')

    def test_total_coast_of_all_items_in_order_without_discount(self):
        self.assertEqual(self.order.get_total_cost(), 30,
                         'Total coast is not valid. Expected {}, got {}'.format(
                             30, self.order.get_total_cost()
                         ))

    def test_total_coast_of_all_items_in_order_wit_ten_present_discount(self):
        self.assertEqual(self.order_sale.get_total_cost(), 22.5,
                         'Total coast is not valid. Expected {}, got {}'.format(
                             30, self.order.get_total_cost()
                         ))

    def test_default_discount_is_zero(self):
        self.assertEqual(self.order.discount, 0, 'Default discount is not zero')


class OrderItemModelTest(BaseModelTestCase):
    """
    Тесты модели товаров входящих в заказ
    """
    def test_default_quantity_is_one(self):
        self.assertEqual(self.order_item_1.quantity, 1,
                         'Default value of quantity is not one')

    def test_coast_of_item_with_many_quantity(self):
        self.assertEqual(self.order_item_2.get_cost(), 25,
                         'Total coast is not valid. Expected {}, got{}'.format(
                             25, self.order_item_2.get_cost()
                         ))

    def test_get_coast_with_default_quantity(self):
        self.assertEqual(self.order_item_1.get_cost(), 5,
                         'Total coast is not valid. Expected {}, got{}'.format(
                             5, self.order_item_2.get_cost()
                         ))

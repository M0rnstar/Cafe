from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from .models import Order

class OrderTestCase(TestCase):
    def setUp(self):
        """
        Создаем тестовые данные: три заказа.
        order1 и order2 имеют статус 'paid' (оплачено), order3 – 'waiting' (в ожидании)
        """
        self.order1 = Order.objects.create(
            table_number=1, 
            status='paid', 
            total_price=Decimal('25.50')
        )
        self.order2 = Order.objects.create(
            table_number=2, 
            status='paid', 
            total_price=Decimal('15.00')
        )
        self.order3 = Order.objects.create(
            table_number=3, 
            status='waiting', 
            total_price=Decimal('30.00')
        )

    def test_create_order(self):
        """
        Проверяет создание заказа через представление add_order.
        Предполагается, что при успешном создании заказа происходит перенаправление (302).
        Для простоты теста передаем только обязательное поле table_number и пустые списки для блюд.
        """
        initial_count = Order.objects.count()
        data = {
            'table_number': 2,
            'dish_name': [],
            'dish_price': [],
        }
        response = self.client.post(reverse('orders:add_order'), data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), initial_count + 1)

    def test_update_order_status(self):
        """
        Проверяет изменение статуса заказа через представление update_order_status.
        При успешном обновлении заказа происходит перенаправление (302).
        """
        data = {
            'status': 'ready'  
        }
        response = self.client.post(
            reverse('orders:update_order_status', kwargs={'order_id': self.order1.pk}),
            data
        )
        self.assertEqual(response.status_code, 302)
        self.order1.refresh_from_db()
        self.assertEqual(self.order1.status, 'ready')

    def test_delete_order(self):
        """
        Проверяет удаление заказа через представление delete_order.
        При успешном удалении происходит перенаправление (302).
        """
        initial_count = Order.objects.count()
        response = self.client.post(
            reverse('orders:delete_order', kwargs={'order_id': self.order1.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), initial_count - 1)

    def test_calculate_revenue(self):
        """
        Проверяет правильность расчета выручки за смену,
        то есть сумму всех заказов со статусом 'paid'.
        """
        response = self.client.get(reverse('orders:calculate_revenue'))
        self.assertEqual(response.status_code, 200)

        expected_revenue = self.order1.total_price + self.order2.total_price
        actual_revenue = response.context.get('total_revenue', Decimal('0.00'))

        self.assertEqual(actual_revenue, expected_revenue)

    def test_invalid_order_creation(self):
        """
        Проверяет, что заказ не создается при отсутствии обязательных данных.
        В данном случае, если поле table_number пустое, форма не проходит валидацию.
        При ошибке валидации представление, как правило, перерендеривает форму с ошибками и возвращает 200.
        """
        initial_count = Order.objects.count()
        data = {
            'table_number': '', 
            'dish_name': [],
            'dish_price': [],
        }
        response = self.client.post(reverse('orders:add_order'), data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), initial_count)

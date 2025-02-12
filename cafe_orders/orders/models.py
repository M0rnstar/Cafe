from django.db import models
from decimal import Decimal
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Order(models.Model):
    STATUS_CHOICES = (
        ('waiting', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено')
    )

    table_number = models.IntegerField(verbose_name="Номер стола")
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Общая стоимость"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='waiting',
        verbose_name="Статус"
    )

    def update_total_price(self):
        """
        Пересчитывает общую стоимость заказа, суммируя цены всех связанных позиций
        """
        total = self.items.aggregate(total=Sum('price'))['total'] or Decimal('0.00') # type: ignore
        self.total_price = total
        self.save(update_fields=['total_price'])

        def __str__(self):
            return f"Заказ {self.id} (Стол {self.table_number})"
        
class OrderItem(models.Model):
        order = models.ForeignKey(
            Order,
            related_name='items',
            on_delete=models.CASCADE,
            verbose_name="Заказ"
        )
        dish_name = models.CharField(max_length=100, verbose_name="Название блюда")
        price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")

        def __str__(self):
            return f"{self.dish_name} - {self.price}"
        

@receiver(post_save, sender=OrderItem)
def update_order_total_on_save(sender, instance, created, **kwards):
     """
     После сохранения позиции заказа пересчитывает общую стоимость соответствующего заказа
     """        
     instance.order.update_total_price()

@receiver(post_delete, sender=OrderItem)
def update_order_total_on_delete(sender, instance, **kwargs):
     """
     После сохранения позиции заказа пересчитывает общую стоимость соответствующего заказа
     """
     instance.order.update_total_price()
    
    
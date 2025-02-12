from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib import messages
from decimal import Decimal
from .models import Order, OrderItem
from .forms import OrderForm

def add_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.status = 'waiting'  
            order.save()
            messages.success(request, "Заказ успешно создан!")
            dish_names = request.POST.getlist('dish_name')
            dish_prices = request.POST.getlist('dish_price')
            for name, price in zip(dish_names, dish_prices):
                if name.strip() == '' or price.strip() == '':
                    continue
                try:
                    price_decimal = Decimal(price)
                except Exception:
                    price_decimal = Decimal('0.00')
                order_item = OrderItem.objects.create(
                    order=order,
                    dish_name=name,
                    price=price_decimal
                )
            return redirect('orders:list_orders')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        order_form = OrderForm()
    return render(request, 'orders/add_order.html', {'order_form': order_form})

def list_orders(request):
    """
    Представление для отображения списка всех заказов.
    Поддерживается фильтрация по номеру стола и статусу.
    """
    orders = Order.objects.all()
    table_number = request.GET.get('table_number')
    status = request.GET.get('status')
    if table_number:
        orders = orders.filter(table_number=table_number)
    if status:
        orders = orders.filter(status=status)
    return render(request, 'orders/list_orders.html', {
        'orders': orders,
        'order_statuses': Order.STATUS_CHOICES,
    })

def update_order_status(request, order_id):
    """
    Представление для изменения статуса заказа.
    При GET-запросе отображается форма для выбора нового статуса.
    При POST – обновляется статус заказа.
    """
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save(update_fields=['status'])
            return redirect('orders:list_orders')
    return render(request, 'orders/update_status.html', {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
    })

def delete_order(request, order_id):
    """
    Представление для удаления заказа.
    Отображает страницу подтверждения удаления.
    """
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('orders:list_orders')
    return render(request, 'orders/delete_order.html', {
        'order': order,
    })

def calculate_revenue(request):
    """
    Представление для расчёта выручки за смену.
    Суммируются заказы со статусом "оплачено".
    """
    orders = Order.objects.filter(status='paid')
    total_revenue = orders.aggregate(total=Sum('total_price'))['total'] or Decimal('0.00')
    return render(request, 'orders/revenue.html', {
        'total_revenue': total_revenue,
    })

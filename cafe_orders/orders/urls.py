from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.list_orders, name='list_orders'),
    path('add/', views.add_order, name='add_order'),
    path('update-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('revenue/', views.calculate_revenue, name='calculate_revenue'),
]

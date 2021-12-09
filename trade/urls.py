from django.urls import path
from trade import views

urlpatterns = [
    path('order', views.OrderAPIView.as_view(), name='order_api_view')
]
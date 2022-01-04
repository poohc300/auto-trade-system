from django.urls import path
from coinone import views

urlpatterns = [
    path('order', views.OrderView.as_view()),
    path('orderbook', views.OrderBookView.as_view()),
    path('account', views.AccountView.as_view()),
    path('transaction_history', views.TransactionHistoryView.as_view()),
    path('orderlist', views.OrderlistView.as_view()),
    path('ordercancel', views.OrderCancelView.as_view())
]
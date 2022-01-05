from django.urls import path
from trade import views

urlpatterns = [
    path('order', views.OrderView.as_view(), name='order_api_view'),
    path('orderbook', views.OrderBookView.as_view(), name='orderbook_view'),
    path('account', views.AccountView.as_view(), name='account_view'),
    path('orderchance', views.OrderChanceView.as_view(), name='orderchance_view'),
    path('orderlist', views.OrderListView.as_view(), name='orderlist_view'),
    path('unfinishedOrderlist', views.UnfinishedOrderListView.as_view(), name='unfinishedOrderlist_view'),
    path('orderCancel', views.OrderCancelView.as_view(), name='orderCancel_view'),
    path('bot', views.BotView.as_view(), name='bot')
]
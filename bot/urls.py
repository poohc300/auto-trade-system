from django.urls import path
from bot import views

urlpatterns = [
    path('bot', views.BotView.as_view(), name='bot'),
    path('bot_trade', views.BotTradeView.as_view(), name='bot_trade'),
    path('filtered_coin', views.create_filtered_coin_list, name='filtered_coin_list'),
    path('off_bot', views.off_bot, name="off the bot")
]
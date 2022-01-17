from rest_framework import serializers
from rest_framework import viewsets
from .models import Bot, TransactionHistory

class BotSerializer(serializers.Serializer):
    '''
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField(max_length=100)
    market = models.CharField(max_length=200)
    coin_balance = models.FloatField(max_length=100)
    volume = models.FloatField(max_length=100)
    is_bid = models.BooleanField()
    status = models.BooleanField()
    created_at = models.DateField(auto_now_add=True)

    '''
    user_id = serializers.CharField(required=True)
    balance = serializers.FloatField(required=True)

    def create(self, validated_data):
        print(validated_data)
        bot = Bot.objects.create(
            user_id=validated_data['user_id'],
            balance=validated_data['balance']
        )

        bot.save()
        return bot

    def get(self):
        bot = Bot.objects.all()

        return bot
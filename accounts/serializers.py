from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework import viewsets
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken



User = get_user_model()

class UserCreateSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    def create(self, validated_data):
        user = User.objects.create(
            user_id=validated_data['user_id'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])

        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        user_id = data.get('user_id', None)
        password = data.get('password', None)
        user = authenticate(user_id=user_id, password=password)
        if user is None:
            return {
                'message' : "404"
            }
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            print(payload)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            print(jwt_token)
            update_last_login(None, user)
        except Exception as e:
            return {
                "error" : e
            }
        return {
            'user_id' : user.user_id,
            'token' : jwt_token
        }


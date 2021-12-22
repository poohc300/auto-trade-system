from typing_extensions import Required


User = get_user_model()

class UserCreateSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    print(username)
    def create(self, validated_data):
        user = User.objects.create(
            user_id=validated_data['user_id'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])

        user.save()
        return user
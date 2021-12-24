from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework import generics # generics class-based view 사용할 계획
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework import viewsets
from rest_framework import serializers

# JWT 사용을 위해 필요

from .models import User, UserManager
from .serializers import UserCreateSerializer, UserLoginSerializer
# 누구나 접근 가능
@permission_classes([AllowAny]) 
class Signup(generics.GenericAPIView):
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    'message' : "sign up success"
                
                },
                    status=status.HTTP_201_CREATED,
            )

@permission_classes([AllowAny])
class Login(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({
                "error" : "request body error"
            }, status=status.HTTP_409_CONFLICT)
            
        if serializer.validated_data['user_id'] == 'None':
            return Response({
                "error" : "user_id is empty"
            }, status=status.HTTP_400_BAD_REQUEST)

        response = {
            "success" : True,
            "user_id" : serializer.data['user_id'],
            "token" : serializer.data['token']
        }
        return Response(
            response, status=status.HTTP_200_OK
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'User'
        fields = "__all__"

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializers_class = UserSerializer
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework import generics # generics class-based view 사용할 계획
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes

# JWT 사용을 위해 필요
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from .models import User, UserManager
from .serializers import UserCreateSerializer
# 누구나 접근 가능
@permission_classes([AllowAny]) 
class Signup(generics.GenericAPIView):

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

    def post(self, request, *args, **kwargs):
        
        user = request.data
        print(user)
        if user['username'] == "None":
            return Response({"message": "fail"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(
            {
                "message" : "login success"
            }
        )


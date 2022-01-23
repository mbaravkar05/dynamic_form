
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

class MyObtainTokenPairView(TokenObtainPairView):
    """
    To login and generate_token 
    """
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    """
    CreateUser view for custom user
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
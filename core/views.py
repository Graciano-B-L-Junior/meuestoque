# users/views.py
from rest_framework import generics, permissions
from .serializers import UserListSerializer, UserRegisterSerializer
from django.contrib.auth.models import User

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]  # <- exige autenticação


from django.http import HttpResponse

def login_view(request):
    return HttpResponse(status=204)
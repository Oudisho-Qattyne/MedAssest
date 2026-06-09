from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import UserSerializer, UserCreateSerializer
from .permissions import IsAdmin

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = UserCreateSerializer  # POST uses create
    search_fields = ['full_name', 'email']
    ordering_fields = ['full_name', 'email', 'created_at']
    filterset_fields = ['role']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        return UserCreateSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    # Optionally add custom claims
    pass
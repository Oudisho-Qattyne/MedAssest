from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import AidProviderCategory, AidProvider
from .serializers import AidProviderCategorySerializer, AidProviderSerializer
from .permissions import IsAdminOrReadOnly

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = AidProviderCategory.objects.all()
    serializer_class = AidProviderCategorySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AidProviderCategory.objects.all()
    serializer_class = AidProviderCategorySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class ProviderListCreateView(generics.ListCreateAPIView):
    queryset = AidProvider.objects.all()
    serializer_class = AidProviderSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class ProviderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AidProvider.objects.all()
    serializer_class = AidProviderSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
from django.urls import path
from .views import CategoryListCreateView, CategoryDetailView, ProviderListCreateView, ProviderDetailView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('providers/', ProviderListCreateView.as_view(), name='provider-list'),
    path('providers/<int:pk>/', ProviderDetailView.as_view(), name='provider-detail'),
]
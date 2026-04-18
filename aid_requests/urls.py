from django.urls import path
from .views import (RequestTypeListCreateView, RequestTypeDetailView,
                    AidRequestListCreateView, AidRequestDetailView,
                    AidRequestProviderListCreateView, AidRequestProviderDetailView)

urlpatterns = [
    path('types/', RequestTypeListCreateView.as_view(), name='reqtype-list'),
    path('types/<int:pk>/', RequestTypeDetailView.as_view(), name='reqtype-detail'),
    path('requests/', AidRequestListCreateView.as_view(), name='request-list'),
    path('requests/<int:pk>/', AidRequestDetailView.as_view(), name='request-detail'),
    path('requests/<int:request_pk>/providers/', AidRequestProviderListCreateView.as_view(), name='req-provider-list'),
    path('providers/<int:pk>/', AidRequestProviderDetailView.as_view(), name='req-provider-detail'),
]
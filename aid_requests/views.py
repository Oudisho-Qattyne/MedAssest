from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch
from .models import AidRequestType, AidRequest, AidRequestProvider
from .serializers import (AidRequestTypeSerializer, AidRequestSerializer,
                          AidRequestCreateUpdateSerializer, AidRequestStatusUpdateSerializer,
                          AidRequestProviderSerializer)
from .permissions import IsDoctorOrAdminForRequests, CanChangeRequestStatus

class RequestTypeListCreateView(generics.ListCreateAPIView):
    queryset = AidRequestType.objects.all()
    serializer_class = AidRequestTypeSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrAdminForRequests]
    search_fields = ['type_name', 'description']
    ordering_fields = ['type_name']

class RequestTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AidRequestType.objects.all()
    serializer_class = AidRequestTypeSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrAdminForRequests]

class AidRequestListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsDoctorOrAdminForRequests]
    search_fields = ['description', 'place_of_aid']
    ordering_fields = ['date_of_aid', 'estimated_cost', 'id']
    filterset_fields = ['request_status', 'patient', 'aid_request_type', 'date_of_aid']

    def get_queryset(self):
        # Prefetch providers to avoid N+1 when calculating total_provided_amount
        return AidRequest.objects.prefetch_related(
            Prefetch('providers', queryset=AidRequestProvider.objects.select_related('aid_provider'))
        ).select_related('patient', 'aid_request_type')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AidRequestCreateUpdateSerializer
        return AidRequestSerializer

    def perform_create(self, serializer):
        serializer.save()

class AidRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsDoctorOrAdminForRequests, CanChangeRequestStatus]

    def get_queryset(self):
        # Same prefetch for detail view
        return AidRequest.objects.prefetch_related(
            Prefetch('providers', queryset=AidRequestProvider.objects.select_related('aid_provider'))
        ).select_related('patient', 'aid_request_type')

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            if 'request_status' in self.request.data:
                return AidRequestStatusUpdateSerializer
            return AidRequestCreateUpdateSerializer
        return AidRequestSerializer

# AidRequestProvider junction endpoints (only admin or doctor can manage)
class AidRequestProviderListCreateView(generics.ListCreateAPIView):
    serializer_class = AidRequestProviderSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrAdminForRequests]
    search_fields = ['notes']
    ordering_fields = ['aid_amount']
    filterset_fields = ['aid_type', 'type_of_aid_amount', 'aid_provider']

    def get_queryset(self):
        return AidRequestProvider.objects.filter(aid_request_id=self.kwargs['request_pk'])

    def perform_create(self, serializer):
        aid_request = AidRequest.objects.get(pk=self.kwargs['request_pk'])
        serializer.save(aid_request=aid_request)

class AidRequestProviderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AidRequestProvider.objects.all()
    serializer_class = AidRequestProviderSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrAdminForRequests]
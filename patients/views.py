from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Patient, FamilyMember
from .serializers import PatientSerializer, PatientCreateUpdateSerializer, FamilyMemberSerializer
from .permissions import IsAdminOrDoctorForPatients
from users.permissions import IsAdmin

class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrDoctorForPatients]
    search_fields = ['first_name', 'middle_name', 'last_name', 'national_number', 'phone_number', 'current_residence']
    ordering_fields = ['first_name', 'last_name', 'birth_date', 'created_at']
    filterset_fields = ['gender', 'marital_status', 'home_status']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PatientCreateUpdateSerializer
        return PatientSerializer

    def perform_create(self, serializer):
        serializer.save(created_by_user=self.request.user)

class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrDoctorForPatients]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return PatientCreateUpdateSerializer
        return PatientSerializer

# Family members – only admin or doctor can manage
class FamilyMemberListCreateView(generics.ListCreateAPIView):
    serializer_class = FamilyMemberSerializer
    permission_classes = [IsAuthenticated, IsAdminOrDoctorForPatients]
    search_fields = ['full_name']
    ordering_fields = ['full_name']
    filterset_fields = ['relation', 'gender']

    def get_queryset(self):
        return FamilyMember.objects.filter(patient_id=self.kwargs['patient_pk'])

    def perform_create(self, serializer):
        patient = Patient.objects.get(pk=self.kwargs['patient_pk'])
        serializer.save(patient=patient)

class FamilyMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FamilyMember.objects.all()
    serializer_class = FamilyMemberSerializer
    permission_classes = [IsAuthenticated, IsAdminOrDoctorForPatients]
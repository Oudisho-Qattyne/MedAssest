from django.urls import path
from .views import PatientListCreateView, PatientDetailView, FamilyMemberListCreateView, FamilyMemberDetailView

urlpatterns = [
    path('', PatientListCreateView.as_view(), name='patient-list'),
    path('<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('<int:patient_pk>/family/', FamilyMemberListCreateView.as_view(), name='family-list'),
    path('family/<int:pk>/', FamilyMemberDetailView.as_view(), name='family-detail'),
]
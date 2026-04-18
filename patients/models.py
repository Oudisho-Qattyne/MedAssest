from django.db import models
from users.models import User

class Patient(models.Model):
    GENDER_CHOICES = (('male', 'Male'), ('female', 'Female'))
    MARITAL_STATUS = (('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'), ('widowed', 'Widowed'))
    HOME_STATUS = (('owned', 'Owned'), ('rented', 'Rented'), ('family_owned', 'Family Owned'))

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    mother_full_name = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    national_number = models.CharField(max_length=100, unique=True, blank=True)
    family_booklet_no = models.CharField(max_length=100, blank=True)
    current_residence = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    telephone_number = models.CharField(max_length=50, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS, blank=True)
    home_status = models.CharField(max_length=20, choices=HOME_STATUS, blank=True)
    job_type = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    special_needs = models.CharField(max_length=200, blank=True)
    note = models.CharField(max_length=200, blank=True)
    created_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_patients')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class FamilyMember(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='family_members')
    full_name = models.CharField(max_length=100)
    relation = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=10, choices=Patient.GENDER_CHOICES, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    note = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.relation})"
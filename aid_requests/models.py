from django.db import models
from patients.models import Patient
from aid_providers.models import AidProvider

class AidRequestType(models.Model):
    type_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.type_name

class AidRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='aid_requests')
    request_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.CharField(max_length=100, blank=True)
    aid_request_type = models.ForeignKey(AidRequestType, on_delete=models.SET_NULL, null=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    place_of_aid = models.CharField(max_length=100, blank=True)
    date_of_aid = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Request #{self.id} for {self.patient}"

class AidRequestProvider(models.Model):
    AID_TYPE_CHOICES = (('medical', 'Medical'), ('financial', 'Financial'))
    AMOUNT_TYPE_CHOICES = (('percentage', 'Percentage'), ('fixed', 'Fixed'))

    aid_request = models.ForeignKey(AidRequest, on_delete=models.CASCADE, related_name='providers')
    aid_provider = models.ForeignKey(AidProvider, on_delete=models.CASCADE)
    aid_type = models.CharField(max_length=20, choices=AID_TYPE_CHOICES, blank=True)
    aid_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    type_of_aid_amount = models.CharField(max_length=20, choices=AMOUNT_TYPE_CHOICES, blank=True)
    notes = models.TextField(blank=True)

    # class Meta:
    #     unique_together = ('aid_request', 'aid_provider')
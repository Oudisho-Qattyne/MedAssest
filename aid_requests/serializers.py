from rest_framework import serializers
from django.db.models import Sum, F, Value, Case, When, FloatField
from django.db.models.functions import Coalesce
from .models import AidRequestType, AidRequest, AidRequestProvider

class AidRequestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AidRequestType
        fields = '__all__'

class AidRequestProviderSerializer(serializers.ModelSerializer):
    provider_name = serializers.ReadOnlyField(source='aid_provider.name')
    class Meta:
        model = AidRequestProvider
        fields = '__all__'
        read_only_fields = ['id']

class AidRequestSerializer(serializers.ModelSerializer):
    providers = AidRequestProviderSerializer(many=True, read_only=True)
    patient_full_name = serializers.ReadOnlyField(source='patient.__str__')
    request_type_name = serializers.ReadOnlyField(source='aid_request_type.type_name')
    total_provided_amount = serializers.SerializerMethodField()

    class Meta:
        model = AidRequest
        fields = '__all__'
        read_only_fields = ['id']

    def get_total_provided_amount(self, obj):
        """
        Calculate total aid amount provided by all assigned providers.
        - Fixed amounts are added directly.
        - Percentage amounts: (percentage / 100) * estimated_cost.
        If estimated_cost is None or 0, percentage contributions are treated as 0.
        """
        total = 0
        estimated = obj.estimated_cost or 0

        for provider_link in obj.providers.all():
            amount = provider_link.aid_amount
            if amount is None:
                continue
            if provider_link.type_of_aid_amount == 'fixed':
                total += amount
            elif provider_link.type_of_aid_amount == 'percentage' and estimated > 0:
                total += (amount / 100) * estimated
        return round(total, 2)

class AidRequestCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AidRequest
        fields = '__all__'
        read_only_fields = ['id', 'request_status']

class AidRequestStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AidRequest
        fields = ['request_status']
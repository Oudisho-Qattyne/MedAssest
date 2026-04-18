from rest_framework import serializers
from .models import AidProviderCategory, AidProvider

class AidProviderCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AidProviderCategory
        fields = '__all__'

class AidProviderSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.category_name')

    class Meta:
        model = AidProvider
        fields = '__all__'
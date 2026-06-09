from rest_framework import serializers
from .models import AidProviderCategory, AidProvider

class AidProviderCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AidProviderCategory
        fields = '__all__'

class AidProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AidProvider
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.category:
            data['category'] = {
                'id': instance.category.id,
                'name': instance.category.category_name
            }
        return data
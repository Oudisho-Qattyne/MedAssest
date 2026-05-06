from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default validation returns the token data dict
        data = super().validate(attrs)
        # Add the user's role to the response
        data['role'] = self.user.role
        return data
from rest_framework import serializers
from .models import DogUser

class DogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return DogUser.objects.create_user(**validated_data)
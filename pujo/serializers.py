from rest_framework import serializers
from django.utils import timezone
from .models import Pujo

class PujoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pujo
        fields = ['id', 'name', 'city', 'address', 'lat','lon','zone']
    
    def create(self, validated_data):
        return Pujo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update fields based on provided data
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.zone = validated_data.get('zone', instance.zone)
        instance.updated_at = timezone.now()
        instance.save()  
        return instance

class TrendingPujoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pujo
        fields = "__all__"

class SearchedPujoSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    class Meta:
        model = Pujo
        fields = ['id']

    
from rest_framework import serializers
from django.utils import timezone
from .models import Pujo
from transport.serializers import TransportReadSerializer

class PujoSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    address = serializers.CharField()
    city = serializers.CharField()
    zone = serializers.CharField()
    class Meta:
        model = Pujo
        fields = ['id', 'lat','lon','zone', 'city', 'name', 'address', 'created_at']
    
    def create(self, validated_data):
        return Pujo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update fields based on provided data
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.zone = validated_data.get('zone', instance.zone)
        instance.lat = validated_data.get('lat', instance.lat)
        instance.lon = validated_data.get('lon', instance.lon)
        # can not update search score from this serializer
        validated_data.pop('search_score', None)
        
        instance.updated_at = timezone.now()
        instance.save()  
        return instance
    
class TrendingPujoSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    zone = serializers.SerializerMethodField()
    transport = TransportReadSerializer()
    class Meta:
        model = Pujo
        fields = ['id', 'lat','lon','zone', 'city', 'name', 'address', 'search_score', 'created_at', 'transport', 'nearest_transport_distance']

class SearchedPujoSerializer(serializers.ModelSerializer):
    ids = serializers.ListField(
        child=serializers.UUIDField(format='hex_verbose'),
        required=True
    )
    term = serializers.ChoiceField(
        choices=['search', 'select', 'navigate'], 
        required=True
    )

    class Meta:
        model = Pujo
        fields = ['ids', 'term']

class searchPujoSerializer(serializers.ModelSerializer):
    term = serializers.CharField()
    class Meta:
        model = Pujo
        fields = ["term"]

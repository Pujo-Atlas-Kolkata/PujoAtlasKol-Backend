from rest_framework import serializers
from .models import Pujo

class PujoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pujo
        fields = ['uuid', 'name', 'city', 'address', 'lat','lon','zone']

class TrendingPujoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pujo
        fields = "__all__"
    

class NewPujoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pujo
        fields = ['name', 'city', 'address', 'lat','lon','zone']
    
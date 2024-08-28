from rest_framework import serializers
from .models import Pujo

class PujoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pujo
        fields = ['uuid', 'name', 'city', 'address', 'lat','lon','zone']

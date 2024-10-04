from rest_framework import serializers
from django.utils import timezone
from .models import Transport
from django.db import models

class TransportSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    station_code = serializers.CharField()
    transport_type = serializers.CharField()

    class Meta:
        model = Transport
        fields = "__all__"
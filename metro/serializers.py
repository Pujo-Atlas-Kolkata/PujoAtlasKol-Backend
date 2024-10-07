from rest_framework import serializers
from django.utils import timezone
from .models import Metro
from django.db import models

class MetroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metro
        fields ="__all__"


class MetroReadSerializer(serializers.ModelSerializer):
     class Meta:
        model = Metro
        fields = ['lat','lon','name','station_code','line']
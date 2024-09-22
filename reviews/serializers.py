from rest_framework import serializers
from .models import Review

class ReviewDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["pujo_id", "user_id", "review", "created_at"]
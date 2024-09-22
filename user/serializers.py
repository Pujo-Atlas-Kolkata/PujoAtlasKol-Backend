from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password",
                  "access_location", "contact", "gender", "birth_date",
                  "profile_picture", "bio", "is_verified","user_type"]
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'username': {'required': True},
            'email': {'required': True},
            'user_type': {'required': True},
        }

    def create(self, validated_data):
        user_type = validated_data.get('user_type','user')
        
        validated_data['user_type'] = user_type
        
        if user_type == 'superadmin':
            validated_data['is_superuser'] = True
            validated_data['is_staff'] = True
        elif user_type == 'admin':
            validated_data['is_superuser'] = False
            validated_data['is_staff'] = True
        else:
            validated_data['is_superuser'] = False
            validated_data['is_staff'] = False

        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

    def update(self, instance, validated_data):
        # Prevent user_type and certain fields from being updated
        for field in ['user_type', 'last_login', 'is_superuser', 'is_staff', 'date_joined',
                      'is_deleted', 'access_token', 'refresh_token', 'groups', 'user_permissions']:
            validated_data.pop(field, None)

        # Extract and handle password
        password = validated_data.pop('password', None)
        email = validated_data.pop('email', None)

        # Update instance with validated data
        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)

        if email:
            instance.email = email
            instance.is_verified = False

        instance.save()
        return instance
    
    def validate(self, attrs):
        # Check for non-deleted users only
        if User.objects.filter(username=attrs.get('username'), is_deleted=False).exists():
            raise serializers.ValidationError({'username': 'A user with this username already exists.'})

        if User.objects.filter(email=attrs.get('email'), is_deleted=False).exists():
            raise serializers.ValidationError({'email': 'A user with this email already exists.'})

        return attrs

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']

class UserLogoutSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    id = serializers.UUIDField()
    class Meta:
        model = User
        fields = ['username','id']

class RefreshTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    id = serializers.UUIDField()
    refresh = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['username','id','refresh']
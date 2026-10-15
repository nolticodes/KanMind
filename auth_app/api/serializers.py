from rest_framework import serializers
from auth_app.models import User


"""Serializers for user registration and authentication."""

from rest_framework import serializers
from auth_app.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Validate and create a new user account."""

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate_email(self, value):
        """Ensure that the provided email address is not already in use."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def validate(self, attrs):
        """Ensure that the password and repeated password match."""
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"error": "Passwords don't match"}
            )
        return attrs

    def create(self, validated_data):
        """Create a user with a securely hashed password."""
        validated_data.pop("repeated_password")
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    """Validate user credentials for the login process."""

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        """Validate the email address and password and attach the user."""
        if not User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError('Email does not exist')

        user = User.objects.filter(email=attrs["email"]).first()

        if not user.check_password(attrs["password"]):
            raise serializers.ValidationError('Password is wrong')
        
        attrs["user"] = user
        return attrs
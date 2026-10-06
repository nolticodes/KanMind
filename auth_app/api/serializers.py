from rest_framework import serializers
from auth_app.models import User


class RegistrationSerializer(serializers.ModelSerializer):

    repeated_password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"error": "Passwords don't match"}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("repeated_password")
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        if not User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError('Email does not exist')

        user = User.objects.filter(email=attrs["email"]).first()

        if not user.check_password(attrs["password"]):
            raise serializers.ValidationError('Password is wrong')
        
        attrs["user"] = user
        return attrs
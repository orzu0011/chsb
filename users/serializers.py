import base64
import io
from django.core.files.base import ContentFile
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User

def password_validator(value):
    if len(value) < 8:
        raise serializers.ValidationError("Parol kamida 8 ta belgidan iborat bo‘lishi kerak.")
    return value

class PasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[password_validator],
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('password',)

class CheckUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, validators=[password_validator])

class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        avatar_data = validated_data.pop('avatar', None)

        if avatar_data:
            img_data = base64.b64decode(avatar_data)
            img = ContentFile(img_data, name="avatar.png")
        else:
            img = None

        if not password:
            raise serializers.ValidationError("Parol talab qilinadi.")

        user = super().create(validated_data)
        user.password = make_password(password)
        user.is_active = False
        user.avatar = img
        user.save()

        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'email', 'username', 'birthday', 'phone', 'user_type', 'password')

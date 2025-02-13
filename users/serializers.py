import base64
import io
from django.core.files import File
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User

# Custom validator for password length
def password_validator(value):
    if len(value) < 8:
        raise serializers.ValidationError("Password must be at least 8 characters long.")
    return value

class PasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[password_validator],
        help_text='Leave empty if no change is needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ('password',)

class CheckUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[password_validator],
        help_text='Leave empty if no change is needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ('username', 'password')

class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(write_only=True)  # Expecting base64 string for avatar image

    def create(self, validated_data):
        password = self.initial_data.get('password', False)
        avatar_data = self.initial_data.get('avatar', False)

        # Check if avatar is provided, decode the base64 string and prepare image file
        if avatar_data:
            img_data = base64.b64decode(avatar_data)
            img = io.BytesIO(img_data)
        else:
            img = None  # You can add handling for default avatar or raise validation error

        # Ensure password is provided
        if not password:
            raise serializers.ValidationError("Password is required")

        # Remove avatar data from validated data before user creation
        validated_data.pop('avatar', None)

        # Create the user instance and set the password
        user = super().create(validated_data)
        user.password = make_password(password)  # Hash password before saving
        user.is_active = False  # You may want to handle this flag based on your logic
        user.avatar = File(name=f"avatar_{user.id}", file=img) if img else None
        user.save()

        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'email', 'username', 'birthday', 'phone', 'user_type')

from rest_framework import serializers
import random
from django.core.mail import send_mail
from rest_framework import serializers
from app.users.models import User, PasswordResetCode
from django.utils import timezone

class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name',
            'last_name',
            'created_at', 'password'
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserProfileSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name',
            'last_name', 'is_active', 'is_staff', 
            'created_at'
        ]


class RequestResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User not found")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        code = str(random.randint(100000, 999999))

        PasswordResetCode.objects.create(user=user, code=code)

        send_mail(
            subject="Password Reset Code",
            message=f"Your reset code: {code}",
            from_email=None,
            recipient_list=[email],
        )


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("code")

        try:
            user = User.objects.get(email=email)
            reset_obj = PasswordResetCode.objects.filter(
                user=user, code=code, is_confirmed=False
            ).latest("created_at")
        except:
            raise serializers.ValidationError("Invalid code")

        if reset_obj.is_expired():
            raise serializers.ValidationError("Code expired")

        reset_obj.is_confirmed = True
        reset_obj.save()

        attrs["user"] = user
        return attrs


class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User not found")
        return value

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.set_password(self.validated_data['password'])
        user.save()
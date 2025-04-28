from rest_framework import serializers
from ...models import User, Profile
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.contrib.auth import get_user_model

# User = get_user_model

class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=250, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password1"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError("Password1 dos not match password")
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)


class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"details": "user does not exist"})
        if user_obj.is_verified:
            raise serializers.ValidationError({"details": "user is already verified"})
        attrs["user"] = user_obj
        return super().validate(attrs)


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
            if not user.is_verified:
                raise serializers.ValidationError(
                    {"details": "user is not verified..."}
                )
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")
        print(user,".........................")
        attrs["user"] = user
        return attrs


class CustomTokenOptainPairSerializer(TokenObtainPairSerializer):
    # def validate(self, attrs):
    #     validated_data = super().validate(attrs)
    #     if not self.user.is_verified:
    #         raise serializers.ValidationError({"details": "user is not verified"})
    #     validated_data["email"] = self.user.email
    #     validated_data["user_id"] = self.user.id
    #     return validated_data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['user_id'] = user.id
        # ...

        return token

    def validate(self, attrs):
        data = super().validate(attrs)  # دریافت توکن‌های اصلی (access و refresh)
        # refresh = self.get_token(self.user)  # ساخت توکن با فیلدهای سفارشی
        # data['refresh'] = str(refresh)
        # data['access'] = str(refresh.access_token)
        
        # اضافه کردن اطلاعات کاربر به پاسخ
        data['user_id'] = self.user.id
        data['email'] = self.user.email
        # data['username'] = self.user.username
        # data['first_name'] = self.user.first_name
        # data['last_name'] = self.user.last_name
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "email", "first_name", "last_name", "image", "description")
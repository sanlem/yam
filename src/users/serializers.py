from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "username"]

    username = serializers.CharField(source="user.username")


class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "username", "blocked", "contacts"]

    username = serializers.CharField(source="user.username")
    contacts = UserSerializer(many=True)
    blocked = UserSerializer(many=True)


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    password1 = serializers.CharField(max_length=20)
    password2 = serializers.CharField(max_length=20)

    def validate(self, attrs):
        pwr1 = attrs["password1"]
        pwr2 = attrs["password2"]

        if not (pwr1 == pwr2 and pwr1):
            raise serializers.ValidationError(
                _("Passwords should be non-empty and equal.")
            )

        return attrs

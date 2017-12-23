from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "username"]

    username = serializers.CharField(source="self.user.username")


class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "username", "blocked", "contacts"]

    username = serializers.CharField(source="self.user.username")
    contacts = UserSerializer(many=True)
    blocked = UserSerializer(many=True)

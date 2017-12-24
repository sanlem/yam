from rest_framework import serializers
from .models import Message, Chat
from users.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "sender", "text", "created_at", "chat"]


class ChatShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"


class ChatFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "name", "participants", "messages"]

    participants = UserSerializer(many=True)
    messages = MessageSerializer(many=True, source="messages.all")

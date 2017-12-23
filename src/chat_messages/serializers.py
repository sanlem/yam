from rest_framework import serializers
from .models import Message, Chat


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "text", "created_at", "chat"]


class ChatFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat

from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "text", "created_at", "chat"]

    # created_at = serializers.DateTimeField(read_only=True)
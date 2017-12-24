from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from .models import Message, Chat
from users.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "sender", "text", "created_at", "chat"]
        read_only_fields = ["sender", "created_at"]

    def validate(self, attrs):
        chat = attrs["chat"]
        user = self.context["request"].user
        if user.profile not in chat.participants.all():
            raise serializers.ValidationError(_("You are not a member of this chat!"))
        return attrs


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

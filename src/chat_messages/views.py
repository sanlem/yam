from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .serializers import MessageSerializer, ChatFullSerializer, ChatShortSerializer
from .models import Message, Chat
from .permissions import IsMessageSenderOrReadOnly, IsInMessageChat, IsInChat


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated, IsMessageSenderOrReadOnly, IsInMessageChat]

    def get_serializer_context(self):
        """
        This will be used to pass request to the serializers
        context as this is mandatory to check if the user could
        send message to provided chat.
        """
        return {"request": self.request}

    def perform_create(self, serializer):
        """
        Populate message sender from current session.
        """
        serializer.save(sender=self.request.user.profile)


class ChatsView(generics.ListCreateAPIView):
    serializer_class = ChatShortSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}

    def get_queryset(self):
        return self.request.user.profile.chats.all()

    def perform_create(self, serializer):
        """
        Here we will automatically add chat creator to chat's
        participants.
        """
        participants = serializer.validated_data["participants"]
        current_user = self.request.user.profile
        if current_user not in participants:
            participants.append(current_user)

        serializer.save(participants=participants)


class ChatDetailView(generics.RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatFullSerializer
    permission_classes = [IsAuthenticated, IsInChat]

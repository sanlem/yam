from rest_framework import viewsets, generics
from .serializers import MessageSerializer, ChatFullSerializer, ChatShortSerializer
from .models import Message, Chat
from .permissions import IsMessageSenderOrReadOnly, IsInMessageChat


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [IsMessageSenderOrReadOnly, IsInMessageChat]

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

    def get_serializer_context(self):
        return {"request": self.request}

    def get_queryset(self):
        return self.request.user.profile.chats.all()


class ChatDetailView(generics.RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatFullSerializer

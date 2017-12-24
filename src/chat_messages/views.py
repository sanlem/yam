from rest_framework import viewsets, generics
from .serializers import MessageSerializer, ChatFullSerializer, ChatShortSerializer
from .models import Message, Chat
from .permissions import IsMessageSenderOrReadOnly, IsInMessageChat


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [IsMessageSenderOrReadOnly, IsInMessageChat]


class ChatsView(generics.ListCreateAPIView):
    serializer_class = ChatShortSerializer

    def get_queryset(self):
        return self.request.user.profile.chats.all()


class ChatDetailView(generics.RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatFullSerializer

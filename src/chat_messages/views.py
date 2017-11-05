from rest_framework import viewsets
from .serializers import MessageSerializer
from .models import Message
from .permissions import IsMessageSenderOrReadOnly


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [IsMessageSenderOrReadOnly]


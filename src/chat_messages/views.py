from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .serializers import MessageSerializer, ChatFullSerializer, \
    ChatShortSerializer
from .models import Message, Chat
from .permissions import IsMessageSenderOrReadOnly, IsInMessageChat, IsInChat


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated, IsMessageSenderOrReadOnly,
                          IsInMessageChat]

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

        # don't add users that blocked the chat creator

        not_blocked_creator = [u for u in participants
                               if current_user not in u.blocked.all()]
        if current_user not in not_blocked_creator:
            not_blocked_creator.append(current_user)

        serializer.save(participants=not_blocked_creator)


class ChatDetailView(generics.RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatFullSerializer
    permission_classes = [IsAuthenticated, IsInChat]

    def get_serializer_context(self):
        """
        I will populate user to filter out messages from its
        ignor list
        """
        return {"request": self.request}


class LeaveChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user.profile

        print(request.data)

        _id = request.data.get("id", None)

        if _id is None:
            return Response({"error": _("Id should be provided.")},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            chat = Chat.objects.get(id=_id)
        except Chat.DoesNotExist:
            return Response({"error": _("Not found")},
                            status=status.HTTP_404_NOT_FOUND)

        if user in chat.participants.all():
            chat.participants.remove(user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"error":
                             _("You are not participant of this chat.")},
                            status=status.HTTP_400_BAD_REQUEST)


class AddToChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user.profile

        chat_id = request.data.get("chat_id", None)

        if chat_id is None:
            return Response({"error": _("Id should be provided.")},
                            status=status.HTTP_400_BAD_REQUEST)

        user_id = request.data.get("user_id", None)

        if chat_id is None:
            return Response({"error": _("Id should be provided.")},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response({"error": _("Chat not found")},
                            status=status.HTTP_404_NOT_FOUND)

        if user not in chat.participants.all():
            return Response({"error":
                             _("You're not participant of this chat")},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                user_to_add = Profile.objects.get(id=user_id)
            except Profile.DoesNotExist:
                return Response({"error": _("User not found.")},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                if user in user_to_add.blocked.all():
                    return Response({"error":
                                     _("You are blocked by this user.")})
                else:
                    chat.participants.add(user_to_add)
                    return Response(status=status.HTTP_200_OK)


@login_required
def main(request):
    return render(request, "main.html")

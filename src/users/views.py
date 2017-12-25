from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import ugettext as _
from .serializers import RegistrationSerializer, FullUserSerializer
from .models import Profile


class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        # set the password
        user.set_password(serializer.validated_data["password1"])
        user.save()

        profile = Profile(user=user)
        profile.save()


class CurrentUserInfoView(RetrieveAPIView):
    serializer_class = FullUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class BlockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        _id = request.data.get("id", None)

        if _id is None:
            return Response({"error": _("Id should be provided.")},
                            status=status.HTTP_400_BAD_REQUEST)

        if _id == request.user.profile.id:
            return Response({"error": _("Cannot block self.")},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            blocked_user = Profile.objects.get(id=_id)
        except Profile.DoesNotExist:
            return Response({"error": _("User not found.")},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            current_user = request.user.profile
            current_user.blocked.add(blocked_user)
            return Response(status=status.HTTP_200_OK)


class UnlockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        _id = request.data.get("id", None)

        if _id is None:
            return Response({"error": _("Id should be provided.")},
                            status=status.HTTP_400_BAD_REQUEST)

        if _id == request.user.profile.id:
            return Response({"error": _("Cannot unlock self.")},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            blocked_user = Profile.objects.get(id=_id)
        except Profile.DoesNotExist:
            return Response({"error": _("User not found.")},
                            status=status.HTTP_404_NOT_FOUND)

        current_user = request.user.profile

        if blocked_user in current_user.blocked.all():
            current_user.blocked.remove(blocked_user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"error": _("Such user not found in blocked.")},
                            status=status.HTTP_404_NOT_FOUND)


class AddToContactsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        _id = request.data.get("id", None)

        if _id is None:
            return Response({"error": _("Id should be provided.")},
                            status=status.HTTP_400_BAD_REQUEST)

        if _id == request.user.profile.id:
            return Response({"error": _("Cannot add self to contacts.")},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            blocked_user = Profile.objects.get(id=_id)
        except Profile.DoesNotExist:
            return Response({"error": _("User not found.")},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            current_user = request.user.profile
            current_user.contacts.add(blocked_user)
            return Response(status=status.HTTP_200_OK)


class RemoveFromContactsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        _id = request.data.get("id", None)

        if _id is None:
            return Response({"error": _("Id should be provided.")},
                            status=status.HTTP_400_BAD_REQUEST)

        if _id == request.user.profile.id:
            return Response({"error": _("Cannot remove self from contacts.")},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            blocked_user = Profile.objects.get(id=_id)
        except Profile.DoesNotExist:
            return Response({"error": _("User not found.")},
                            status=status.HTTP_404_NOT_FOUND)

        current_user = request.user.profile

        if blocked_user in current_user.blocked.all():
            current_user.contacts.remove(blocked_user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"error": _("Such user not found in blocked.")},
                            status=status.HTTP_404_NOT_FOUND)

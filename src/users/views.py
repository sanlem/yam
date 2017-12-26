from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from .serializers import RegistrationSerializer, FullUserSerializer, \
    UserSerializer
from .models import Profile
from .forms import RegistrationForm


class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        # set the password
        user.set_password(serializer.validated_data["password1"])
        user.save()

        profile = Profile(user=user)
        profile.save()


class AllUsersView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.exclude(id=self.request.user.profile.id)


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

        if blocked_user in current_user.contacts.all():
            current_user.contacts.remove(blocked_user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"error": _("Such user not found in contacts.")},
                            status=status.HTTP_404_NOT_FOUND)


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})

from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
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

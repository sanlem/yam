from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def save(self, commit=True):
        instance = super().save(commit=True)

        p = Profile()
        p.user = instance
        p.save()
        return instance

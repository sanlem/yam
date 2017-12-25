from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    class Meta:
        verbose_name = _("User's profiles")
        verbose_name_plural = _("Users profiles")
        # app_label = "users"

    user = models.OneToOneField(User, related_name="profile")
    blocked = models.ManyToManyField("self", symmetrical=False, blank=True,
                                     verbose_name=_("Blocked users"),
                                     related_name="blocked_by")
    contacts = models.ManyToManyField("self", symmetrical=False, blank=True,
                                      verbose_name=_("User's contacts"),
                                      related_name="contact_of")

    def __str__(self):
        return self.user.username

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Chat(models.Model):
    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    PRIVATE = "private"
    GROUP = "group"

    name = models.CharField(max_length=25, null=True, blank=True,
                            verbose_name=_("Chat room name"))

    room_type = models.CharField(choices=[
        (PRIVATE, _("Private hat")),
        (GROUP, _("Group chat"))
    ], max_length=len(PRIVATE), verbose_name=_("Chat room type"))

    participants = models.ManyToManyField("users.Profile", related_name="chats",
                                          verbose_name=_("Participants"))

    def __str__(self):
        return "Chat {}".format(self.name)


class Message(models.Model):
    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ["created_at"]

    chat = models.ForeignKey(Chat, related_name="message",
                             verbose_name=_("Chat"))

    sender = models.ForeignKey("users.Profile", related_name="out_messages",
                               blank=True,
                               verbose_name=_("Message sender"))

    receiver = models.ForeignKey("users.Profile", related_name="in_messages",
                                 blank=True,
                                 verbose_name=_("Message receiver"))

    text = models.TextField(max_length=500, verbose_name=_("Message text"))
    created_at = models.DateTimeField(editable=False, auto_now_add=True)

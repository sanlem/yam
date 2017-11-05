from django.test import mock
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from chat_messages.models import Message, Chat
from users.models import User, Profile


class MessagesAPITestCase(APITestCase):
    def setUp(self):
        user1 = User.objects.create_user("user1", email="user1@mail.com",
                                         password="12333")
        user2 = User.objects.create_user("user2", email="user2@mail.com",
                                         password="12333")
        self.profile1 = Profile.objects.create(user=user1)
        self.profile2 = Profile.objects.create(user=user2)

        self.client = APIClient()
        self.chat = Chat.objects.create(name="kek", room_type=Chat.PRIVATE)

    def test_message_creation_with_good_data(self):
        count_before_post = Message.objects.count()

        self.client.post(reverse("message-list"), {
            "sender": self.profile1.id, "receiver": self.profile2.id,
            "chat": self.chat.id, "text": "atata"
        }, format="json")

        count_after_post = Message.objects.count()
        self.assertEqual(count_after_post - count_before_post, 1)

    @mock.patch("chat_messages.models.Message.save")
    def test_message_creation_with_bad_data(self, save_mock):
        self.client.post(reverse("message-list"), {
            "sender": self.profile1.id, "receiver": "atatata",
            "chat": self.chat.id, "text": "atata"
        }, format="json")

        # save_mock should not be called
        save_mock.assert_not_called()
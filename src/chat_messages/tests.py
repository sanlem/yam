from django.test import mock
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
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
        self.chat = Chat.objects.create(name="kek")
        self.chat.participants.add(self.profile1)
        self.chat.participants.add(self.profile2)

        self.client.force_authenticate(user=user1)

    def test_message_creation_with_good_data(self):
        count_before_post = Message.objects.count()

        response = self.client.post(reverse("message-list"), {
            # "sender": self.profile1.id,
            "chat": self.chat.id, "text": "atata"
        }, format="json")

        print(response.data)
        count_after_post = Message.objects.count()
        self.assertEqual(count_after_post - count_before_post, 1)

    def test_send_message_to_unreal_chat(self):
        response = self.client.post(reverse("message-list"), {
            "chat": 100500, "text": "atata"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_messages_from_ignored_users(self):
        # create message from second user in this chat
        message = Message(sender=self.profile2, chat_id=self.chat.id,
                          text="aasdasdasd")
        message.save()

        # ensure msg is created
        chat = self.client.get(reverse("chats-detail", args=[self.chat.id]))

        message_ids = [m["id"] for m in chat.data["messages"]]

        self.assertIn(message.id, message_ids)

        # now the first user adds the second user to ignor list
        self.profile1.blocked.add(self.profile2)

        # rerun request
        chat = self.client.get(reverse("chats-detail", args=[self.chat.id]))

        message_ids = [m["id"] for m in chat.data["messages"]]

        self.assertNotIn(message.id, message_ids)

        # remove from ignored
        self.profile1.blocked.remove(self.profile2)

    def test_chat_creation_by_blocked_user(self):
        # user2 adds user1 to ignor
        self.profile2.blocked.add(self.profile1)

        chat_data = {
            "name": "aaaa",
            "participants": [self.profile1.id, self.profile2.id]
        }
        response = self.client.post(reverse("chats-list"), chat_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        participants = response.data["participants"]
        self.assertIn(self.profile1.id, participants)
        self.assertNotIn(self.profile2.id, participants)

        self.profile2.blocked.remove(self.profile1)

    def test_add_to_chat_not_ignored(self):
        chat_data = {
            "name": "aaaa"
        }
        response = self.client.post(reverse("chats-list"), chat_data)

        chat_id = response.data["id"]

        self.assertNotIn(self.profile2.id, response.data["participants"])

        response = self.client.post(reverse("chats-add"),
                                    {"chat_id": chat_id,
                                     "user_id": self.profile2.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # request chat and check
        chat = Chat.objects.get(id=chat_id)

        self.assertIn(self.profile2, chat.participants.all())

    def test_add_to_chat_by_ignored(self):
        self.profile2.blocked.add(self.profile1)

        chat_data = {
            "name": "aaaa"
        }
        response = self.client.post(reverse("chats-list"), chat_data)

        chat_id = response.data["id"]

        self.assertNotIn(self.profile2.id, response.data["participants"])

        response = self.client.post(reverse("chats-add"), {"chat_id": chat_id,
                                                           "user_id": self.profile2.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # request chat and check
        chat = Chat.objects.get(id=chat_id)

        self.assertNotIn(self.profile2, chat.participants.all())

    def test_chat_creator_added_to_participants(self):
        # create chat without participants provided
        response = self.client.post(reverse("chats-list"), {"name": 1})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        participants = response.data["participants"]
        self.assertIn(self.profile1.id, participants)

    def test_leave_chat(self):
        response = self.client.post(reverse("chats-leave"), {"id": self.chat.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.chat.refresh_from_db()
        self.assertNotIn(self.profile1, self.chat.participants.all())

    def test_leave_unreal_chat(self):
        response = self.client.post(reverse("chats-leave"), {"id": 100500})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @mock.patch("chat_messages.models.Message.save")
    def test_message_creation_with_bad_data(self, save_mock):
        self.client.post(reverse("message-list"), {
            "sender": self.profile1.id,
            "chat": "atata", "text": "atata"
        }, format="json")

        # save_mock should not be called
        save_mock.assert_not_called()

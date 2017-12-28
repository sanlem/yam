from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from users.models import Profile


class ProfileTestCase(APITestCase):
    def setUp(self):
        user1 = User.objects.create_user("user1", email="user1@mail.com",
                                         password="12333")
        user2 = User.objects.create_user("user2", email="user2@mail.com",
                                         password="12333")
        self.profile1 = Profile.objects.create(user=user1)
        self.profile2 = Profile.objects.create(user=user2)

        self.client = APIClient()
        self.client.force_authenticate(user1)

    def test_profile(self):
        self.profile1.contacts.add(self.profile2)

        self.assertIn(self.profile2, self.profile1.contacts.all())
        self.assertNotIn(self.profile1, self.profile2.contacts.all())

    def test_block_user(self):
        response = self.client.post(reverse("users-block"), {"id": self.profile2.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.profile1.refresh_from_db()
        self.assertIn(self.profile2, self.profile1.blocked.all())

        # now unlock
        response = self.client.post(reverse("users-unlock"), {"id":self.profile2.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.profile1.refresh_from_db()
        self.assertNotIn(self.profile2, self.profile1.blocked.all())

    def test_block_invalid_user(self):
        response = self.client.post(reverse("users-block"), {"id": 100500})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_block_user_no_id_provided(self):
        response = self.client.post(reverse("users-block"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_to_contacts(self):
        response = self.client.post(reverse("users-add-to-contacts"), {"id": self.profile2.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.profile1.refresh_from_db()
        self.assertIn(self.profile2, self.profile1.contacts.all())

        # now remove
        response = self.client.post(reverse("users-remove-from-contacts"),
                                    {"id":self.profile2.id})
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.profile1.refresh_from_db()
        self.assertNotIn(self.profile2, self.profile1.blocked.all())

    def test_add_to_contacts_invalid_user(self):
        response = self.client.post(reverse("users-add-to-contacts"), {"id": 100500})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_to_contacts_user_no_id_provided(self):
        response = self.client.post(reverse("users-add-to-contacts"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile


class ProfileTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user("user1", email="user1@mail.com",
                                         password="12333")
        user2 = User.objects.create_user("user2", email="user2@mail.com",
                                         password="12333")
        self.profile1 = Profile.objects.create(user=user1)
        self.profile2 = Profile.objects.create(user=user2)

    def test_profile(self):
        self.profile1.contacts.add(self.profile2)

        self.assertIn(self.profile2, self.profile1.contacts.all())
        self.assertNotIn(self.profile1, self.profile2.contacts.all())

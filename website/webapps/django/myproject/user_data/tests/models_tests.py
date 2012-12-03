"""Tests for the models of the ``user_data`` app."""
from django.test import TestCase

from user_data.tests.factories import UserProfileFactory


class PersonalProfileTestCase(TestCase):
    """Tests for the ``PersonalProfile`` model class."""
    def setUp(self):
        self.profile = UserProfileFactory()

    def test_model(self):
        self.assertTrue(self.profile.pk, msg=(
            'Should be able to create and save a PersonalProfile'))

"""Factories for the ``user_data`` app."""
import factory

from user_data import models
from django_libs.tests.factories import UserFactory


class UserProfileFactory(factory.Factory):
    FACTORY_FOR = models.UserProfile

    user = factory.SubFactory(UserFactory)

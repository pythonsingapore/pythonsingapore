"""Factories for the ``user_data`` app."""
import factory

from user_data import models
from django_libs.tests.factories import UserFactory


class UserProfileFactory(factory.Factory):
    FACTORY_FOR = models.UserProfile

    user = factory.SubFactory(UserFactory)


class UndergraduateDegreeFactory(factory.Factory):
    FACTORY_FOR = models.UndergraduateDegree

    user = factory.SubFactory(UserFactory)
    field_of_study = 'Field of study'


class PersonalProfileFactory(factory.Factory):
    FACTORY_FOR = models.PersonalProfile

    user = factory.SubFactory(UserFactory)
    last_name = 'Smith'
    first_name = 'John'


class PostgraduateDegreeFactory(factory.Factory):
    FACTORY_FOR = models.PostgraduateDegree

    user = factory.SubFactory(UserFactory)
    field_of_study = 'Field of study'


class WorkExperienceFactory(factory.Factory):
    FACTORY_FOR = models.WorkExperience

    user = factory.SubFactory(UserFactory)
    job_title = 'Job title'

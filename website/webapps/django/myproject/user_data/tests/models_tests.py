"""Tests for the models of the ``user_data`` app."""
import datetime

from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from user_data.models import append_year, PersonalProfile
from user_data.tests.factories import (
    PersonalProfileFactory,
    PostgraduateDegreeFactory,
    UndergraduateDegreeFactory,
    UserProfileFactory,
    WorkExperienceFactory,
)


class AppendYearTestCase(TestCase):
    """Tests for the ``append_year`` function."""
    def test_function(self):
        obj = WorkExperienceFactory()
        result = append_year(obj, 'foo')
        self.assertEqual(result, 'foo', msg=(
            'When no dates given, nothing should be appended'))

        obj.start_date = datetime.date(2000, 01, 01)
        result = append_year(obj, 'foo')
        self.assertEqual(result, 'foo (2000)', msg=(
            'When only start date given, it should be appended'))

        obj.start_date = None
        obj.end_date = datetime.date(2010, 01, 01)
        result = append_year(obj, 'foo')
        self.assertEqual(result, 'foo (2010)', msg=(
            'When only end date given, it should be appended'))

        obj.start_date = datetime.date(2000, 01, 01)
        result = append_year(obj, 'foo')
        self.assertEqual(result, 'foo (2000 - 2010)', msg=(
            'When both dates given, they should be appended'))


class PersonalProfileTestCase(TestCase):
    """Tests for the ``PersonalProfile`` model class."""
    def setUp(self):
        self.profile = PersonalProfileFactory()

    def test_model(self):
        self.assertTrue(self.profile.pk, msg=(
            'Should be able to create and save a PersonalProfile'))


class PostgraduateDegreeTestCase(TestCase):
    """Tests for the ``PostgraduateDegree`` model class."""
    def setUp(self):
        self.object = PostgraduateDegreeFactory()

    def test_model(self):
        self.assertTrue(self.object.pk, msg=(
            'Should be able to create and save the objet'))

    def test_get_display_string(self):
        result = self.object.get_display_string()
        self.assertEqual(result, "%s (%s)" % (self.object.field_of_study,
                                              _('ongoing')))

        self.object.end_date = datetime.date(2000, 01, 01)
        result = self.object.get_display_string()
        self.assertEqual(result, "%s (%s)" % (self.object.field_of_study,
                                              self.object.end_date))


class UndergraduateDegreeTestCase(TestCase):
    """Tests for the ``UndergraduateDegree`` model class."""
    def setUp(self):
        self.object = UndergraduateDegreeFactory()

    def test_model(self):
        self.assertTrue(self.object.pk, msg=(
            'Should be able to create and save the objet'))

    def test_get_display_string(self):
        result = self.object.get_display_string()
        self.assertEqual(result, "%s (%s)" % (self.object.field_of_study,
                                              _('ongoing')))

        self.object.end_date = datetime.date(2000, 01, 01)
        result = self.object.get_display_string()
        self.assertEqual(result, "%s (%s)" % (self.object.field_of_study,
                                              self.object.end_date))


class UserProfileTestCase(TestCase):
    """Tests for the ``UserProfile`` model class."""
    def setUp(self):
        self.profile = UserProfileFactory()

    def test_model(self):
        self.assertTrue(self.profile.pk, msg=(
            'Should be able to create and save a UserProfile'))

    def test_get_personal_profile(self):
        self.profile.get_personal_profile()
        self.assertEqual(PersonalProfile.objects.all().count(), 1, msg=(
            'Should create a new PersonalProfile when called for the first'
            ' time'))

    def test_get_postgraduate_degrees(self):
        result = self.profile.get_postgraduate_degrees()
        self.assertEqual(result.count(), 0, msg=(
            'Should return the PostgraduateDegree resultset for this user'))

    def test_get_undergraduate_degrees(self):
        result = self.profile.get_undergraduate_degrees()
        self.assertEqual(result.count(), 0, msg=(
            'Should return the UndergraduateDegree resultset for this user'))

    def test_get_work_experiences(self):
        result = self.profile.get_work_experiences()
        self.assertEqual(result.count(), 0, msg=(
            'Should return the WorkExperience resultset for this user'))


class WorkExperienceTestCase(TestCase):
    """Tests for the ``WorkExperience`` model class."""
    def setUp(self):
        self.object = WorkExperienceFactory()

    def test_model(self):
        self.assertTrue(self.object.pk, msg=(
            'Should be able to create and save the objet'))

    def test_get_display_string(self):
        result = self.object.get_display_string()
        self.assertEqual(result, "%s (%s)" % (self.object.company_name,
                                              _('ongoing')))

        self.object.end_date = datetime.date(2000, 01, 01)
        result = self.object.get_display_string()
        self.assertEqual(result, "%s (%s)" % (self.object.company_name,
                                              self.object.end_date))

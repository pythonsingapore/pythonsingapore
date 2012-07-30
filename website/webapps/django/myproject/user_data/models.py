"""Models for the ``user_data`` app."""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    """
    Holds settings that the user has set for himself.

    :user: The user this profile belongs to.

    """
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
    )

    def __unicode__(self):
        return '%s' % self.user.email or self.user.username

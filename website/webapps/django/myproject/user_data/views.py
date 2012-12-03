"""Views for the ``user_data`` app."""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic import (
    DetailView,
)
from django.shortcuts import redirect

from user_data.models import UserProfile


class UserDataDetailView(DetailView):
    """
    Shows an overview over all available user data objects.

    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        try:
            self.profile = self.user.get_profile()
        except UserProfile.DoesNotExist:
            try:
                self.user.groups.get(name='translators')
                return redirect(reverse('admin:index'))
            except Group.DoesNotExist:
                pass
            self.profile = UserProfile.objects.create(user=self.user)
        return super(
            UserDataDetailView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.profile

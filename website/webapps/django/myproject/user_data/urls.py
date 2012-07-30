"""URLs for the ``user_data`` app."""
from django.conf.urls.defaults import patterns, url

from user_data.views import (
    UserDataDetailView,
)


urlpatterns = patterns('',
    url(r'^$',
        UserDataDetailView.as_view(),
        name='user_data_detail',
    ),
)

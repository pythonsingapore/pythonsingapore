"""Admin sites for the ``user_data`` app."""
from django.contrib import admin

from user_data import models


class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', )


admin.site.register(models.UserProfile, UserProfileAdmin)

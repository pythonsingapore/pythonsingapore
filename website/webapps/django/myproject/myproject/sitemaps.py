"""Sitemaps that are global to the project (i.e. the django-cms pages)."""
from django.contrib.sitemaps import Sitemap

from cmsplugin_blog.models import EntryTitle


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return EntryTitle.objects.filter(entry__is_published=True)

    def lastmod(self, obj):
        return obj.entry.pub_date

    def location(self, obj):
        location = obj.get_absolute_url()
        return location

"""Sitemaps that are global to the project (i.e. the django-cms pages)."""
from django.contrib.sitemaps import Sitemap

from cms.utils.moderator import get_page_queryset
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


class PagesSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.4

    def items(self):
        page_queryset = get_page_queryset(None)
        all_pages = page_queryset.published().filter(login_required=False)
        return all_pages

    def lastmod(self, page):
        pass

    def location(self, obj):
        location = obj.get_absolute_url()
        return location

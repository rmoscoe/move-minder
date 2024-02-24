from django.conf import settings
from django.contrib import sitemaps
from django.urls import reverse
from urllib.parse import urlparse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "daily"

    def __init__(self, request_site=None, current_site=None):
        super().__init__()
        self.request_site = request_site
        self.current_site = current_site

    def items(self):
        return ["tracker:home", "tracker:sign-up", "tracker:login", "tracker:dashboard", "tracker:parcel-scan"]

    def location(self, item):
        return reverse(item)

    def get_urls(self, page=1, site=None, protocol=None):
        urls = super().get_urls(page, site, protocol)
        if settings.DEBUG:
            domain = settings.DOMAIN
            for url in urls:
                path = urlparse(url["location"]).path
                url["location"] = f"{"http"}://{domain}{path}"
        return urls

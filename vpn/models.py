from urllib.parse import urlparse

from django.contrib.auth.models import AbstractUser
from django.db import models

from vpn import settings


class User(AbstractUser):
    first_name = models.CharField(blank=False)
    last_name = models.CharField(blank=False)
    age = models.PositiveIntegerField(null=True)


class Site(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    url = models.CharField(blank=False)
    title = models.CharField(blank=False)
    visit_count = models.PositiveIntegerField(default=0)
    data_sent = models.PositiveBigIntegerField(default=0)
    data_received = models.PositiveBigIntegerField(default=0)

    class Meta:
        app_label = "vpn"

    @property
    def proxy_url(self):
        parsed_url = urlparse(self.url)
        return parsed_url.path.strip("/")

    @property
    def original_url(self):
        parsed_url = urlparse(self.url)

        scheme = parsed_url.scheme or "https"

        return f"{scheme}://{parsed_url.netloc}/"

    @property
    def data_sent_mb(self):
        return round(int(self.data_sent) / 1000000, 3)

    @property
    def data_received_mb(self):
        return round(int(self.data_received) / 1000000, 3)

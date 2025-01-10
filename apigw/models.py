from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.contrib.auth.models import Group
from encrypted_model_fields.fields import EncryptedCharField
from datetime import datetime
from django.contrib.auth.models import Group

today = datetime.now()
today_path = today.strftime("%Y/%m/%d/%H")


class APIService(models.Model):

    SERVICE_TYPE = (
        (1, "AWS (AWSRequestsAuth)"),
        (2, "HTTP/s Request (GET)"),
        (3, "HTTP/s Request (POST)"),
        (4, "OAuth2 Bearer (GET)"),
    )

    service_slug_url = models.CharField(
        unique=True,
        max_length=1024,
        help_text="Choose a url slug name which will binded to this api, eg(dbca-locations-data)",
    )
    service_type = models.IntegerField(choices=SERVICE_TYPE, default=0)
    service_endpoint_url = models.CharField(
        max_length=1024, help_text="URL of the API service to connect into", default=""
    )

    # Basic Auth (For Service type 2,3)
    basic_auth_enabled = models.BooleanField(default=False)
    basic_auth_username = EncryptedCharField(
        max_length=512, default="", blank=True, null=True
    )
    basic_auth_password = EncryptedCharField(
        max_length=512, default="", blank=True, null=True
    )

    # AWS Information (Service type 1)
    aws_access_key = EncryptedCharField(
        max_length=256, default="", blank=True, null=True
    )
    aws_secret_access_key = EncryptedCharField(
        max_length=256, default="", blank=True, null=True
    )
    aws_token = models.CharField(max_length=256, default="", blank=True, null=True)
    aws_host = models.CharField(max_length=256, default="", blank=True, null=True)
    aws_region = models.CharField(max_length=256, default="", blank=True, null=True)
    aws_service = models.CharField(max_length=256, default="", blank=True, null=True)

    # Oauth2 Bearer Token
    oauth2_url = models.CharField(max_length=256, default="", blank=True, null=True)
    oauth2_client_id = models.CharField(
        max_length=256, default="", blank=True, null=True
    )
    oauth2_secret = models.CharField(max_length=256, default="", blank=True, null=True)

    # oauth2_api_url=models.CharField(max_length=256, default='', blank=True, null=True)
    oauth2_api_ocp_apim_subscription_key = models.CharField(
        max_length=256, default="", blank=True, null=True
    )

    # HTTP Auth Request

    # Cache Requests
    cache_enabled = models.BooleanField(default=True)
    cache_limit = models.IntegerField(
        help_text="Cache expiry limit in seconds", default=60
    )

    # Network Restrictions
    network_restriction_enabled = models.BooleanField(default=True)
    allowed_ips = models.TextField(
        null=True,
        blank=True,
        default="",
        help_text="Use network ranges format: eg 1 ip = 10.1.1.1/32 or for a c class block of ips use 192.168.1.0/24 etc. Each range should be on it own line.",
    )

    # Throttling
    throttling_enabled = models.BooleanField(default=True)
    throttle_limit = models.IntegerField(
        help_text="Query throttle limit per client IP (Request Count)", default=20
    )
    throttle_period = models.IntegerField(
        help_text="Time limit for throttle limit (in seconds) ", default=60
    )

    # Notes
    notes = models.TextField(null=True, blank=True, default="")

    # Group Permissions
    group = models.ForeignKey(
        Group, blank=True, null=True, related_name="group", on_delete=models.SET_NULL
    )

    created = models.DateTimeField(auto_now_add=True, blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return "{}".format(self.service_slug_url)


class APIServiceLog(models.Model):
    api_service = models.ForeignKey(
        APIService,
        blank=True,
        null=True,
        related_name="api_service_id",
        on_delete=models.SET_NULL,
    )
    service_slug_url = models.CharField(max_length=1024)
    server_ip = models.CharField(max_length=100, null=True, blank=True)
    client_ip = models.CharField(max_length=100, null=True, blank=True)
    parameters_get = models.TextField(null=True, blank=True, default="")
    parameters_post = models.TextField(null=True, blank=True, default="")
    parameters_urlappendGET = models.TextField(null=True, blank=True, default="")
    error = models.CharField(max_length=1024, null=True, blank=True)
    allowed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

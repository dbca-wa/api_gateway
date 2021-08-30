from django.contrib import messages
from django.contrib.gis import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from django.db.models import Q

from apigw import models

@admin.register(models.APIService)
class APIService(admin.ModelAdmin):
    list_display = ('id','service_slug_url','service_type','service_endpoint_url',)
    list_filter = ('enabled',)
    search_fields = ('service_slug_url','service_endpoint_url',)




from django.contrib import admin

from apps.Organization.models import Organization, OrganizationImage

# Register your models here.
admin.site.register(Organization)
admin.site.register(OrganizationImage)
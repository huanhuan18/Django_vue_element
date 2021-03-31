from django.contrib import admin
from myblog.models import Siteinfo
# Register your models here.
@admin.register(Siteinfo)
class SiteinfoAdmin(admin.ModelAdmin):
    pass
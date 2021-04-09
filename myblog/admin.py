from django.contrib import admin
from myblog.models import Siteinfo, Classes, Userinfo
# Register your models here.
@admin.register(Siteinfo)
class SiteinfoAdmin(admin.ModelAdmin):
    pass
@admin.register(Classes)
class SiteinfoAdmin(admin.ModelAdmin):
    pass
@admin.register(Userinfo)
class SiteinfoAdmin(admin.ModelAdmin):
    pass
from django.contrib import admin
from . import models
# Register your models here.


class SocialAccountInline(admin.StackedInline):
    model = models.SocialAccount
    extra = 1


@admin.register(models.SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    inlines = [
        SocialAccountInline
    ]

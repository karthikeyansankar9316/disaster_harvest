from django.contrib import admin
from .models import User, Disaster, Agency, Citizen, FundRequest, CommunityPost

admin.site.register(User)
admin.site.register(Disaster)
admin.site.register(Agency)
admin.site.register(Citizen)
admin.site.register(FundRequest)
admin.site.register(CommunityPost)


class DisasterAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "severity", "date")
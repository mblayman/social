from django.contrib import admin

from .models import Invite


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ("id", "from_user", "to_user", "status")
    list_filter = ("status",)
    raw_id_fields = ("from_user", "to_user")

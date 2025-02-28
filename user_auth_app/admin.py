from django.contrib import admin
from user_auth_app.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "location",
                    "tel", "created_at", "updated_at")
    search_fields = ("user__username", "user__email", "location", "tel")
    list_filter = ("type", "created_at")

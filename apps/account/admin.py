from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "is_active")
    search_fields = ("email", "user_name")
    readonly_fields = ("activation_code",)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not obj:
            fieldsets = (
                (None, {"fields": ("email", "password")}),
                (
                    "Personal Info",
                    {
                        "fields": (
                            "username",
                            "email",
                            "phone_number",
                            "role",
                            "is_active",
                        )
                    },
                ),
            )
        else:
            fieldsets = (
                (None, {"fields": ("email",)}),
                (
                    "Personal Info",
                    {
                        "fields": (
                            "username",
                            "email",
                            "phone_number",
                            "role",
                            "is_active",
                        )
                    },
                ),
            )
        return fieldsets


admin.site.register(User, UserAdmin)

from django.contrib import admin
from .models import Purchase

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_display",
        "crypto",
        "usd_amount",
        "fee",
        "total",
        "crypto_amount",
        "contact_method",
        "whatsapp_number",
        "email",          # <-- this is your BooleanField
        "created_at",
    )
    list_filter = ("contact_method", "crypto", "email", "created_at")
    search_fields = ("crypto", "whatsapp_number", "user__email")

    def user_display(self, obj):
        # Show the user's email if available, otherwise fallback to user id
        return getattr(obj.user, "email", f"User {obj.user.id}")
    user_display.short_description = "User"

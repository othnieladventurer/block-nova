from django.contrib import admin
from .models import Purchase, SellTransaction





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
        "crypto_address",  
        "email",           
        "status",          
        "created_at",
    )
    list_filter = ("contact_method", "crypto", "email", "status", "created_at")
    search_fields = ("crypto", "whatsapp_number", "crypto_address", "user__email")

    def user_display(self, obj):
        # Show the user's email if available, otherwise fallback to user id
        return getattr(obj.user, "email", f"User {obj.user.id}")
    user_display.short_description = "User"









@admin.register(SellTransaction)
class SellTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "crypto",
        "usd_amount",
        "crypto_amount",
        "net_usd",
        "net_htg",
        "receive_method",
        "status",
        "created_at",
    )
    list_filter = ("status", "receive_method", "crypto", "created_at")
    search_fields = ("user__username", "user__email", "first_name", "last_name", "moncash_number")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Informations générales", {
            "fields": ("user", "crypto", "usd_amount", "crypto_amount", "net_usd", "net_htg", "status")
        }),
        ("Méthode de réception", {
            "fields": ("receive_method", "first_name", "last_name", "address", "phone_number", "moncash_number")
        }),
        ("Preuve de transfert", {
            "fields": ("screenshot",)
        }),
        ("Dates", {
            "fields": ("created_at", "updated_at")
        }),
    )






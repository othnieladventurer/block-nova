from django.db import models
from django.db import models
from customusers.models import CustomUser as User
from django.conf import settings



class Purchase(models.Model):
    CONTACT_CHOICES = [
        ("email", "Email"),
        ("whatsapp", "WhatsApp"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
        ("sent", "Sent"),
        ("delivered", "Delivered"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.CharField(max_length=50)
    usd_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=6)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    crypto_amount = models.DecimalField(max_digits=20, decimal_places=8)
    price_at_purchase = models.DecimalField(max_digits=20, decimal_places=2)
    contact_method = models.CharField(
        max_length=20,
        choices=CONTACT_CHOICES,
        default="email"
    )
    whatsapp_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Enter WhatsApp number if contact method is WhatsApp"
    )
    email = models.BooleanField(
        default=False,
        help_text="Indicates whether the user's email has been verified for this purchase"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        help_text="Current status of the purchase"
    )
    crypto_address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Wallet address where crypto will be sent"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} bought {self.crypto_amount} {self.crypto} via {self.contact_method} [{self.status}]"










class SellTransaction(models.Model):
    METHOD_CHOICES = [
        ("western_union", "Western Union"),
        ("moncash", "MonCash"),
    ]

    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("processing", "En cours"),
        ("completed", "Complété"),
        ("failed", "Échoué"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sell_transactions")
    crypto = models.CharField(max_length=50)  # ex: bitcoin, ethereum
    usd_amount = models.DecimalField(max_digits=12, decimal_places=2)
    crypto_amount = models.DecimalField(max_digits=18, decimal_places=8)
    net_usd = models.DecimalField(max_digits=12, decimal_places=2)
    net_htg = models.DecimalField(max_digits=12, decimal_places=2)

    receive_method = models.CharField(max_length=20, choices=METHOD_CHOICES)

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    moncash_number = models.CharField(max_length=20, blank=True, null=True)

    screenshot = models.ImageField(upload_to="sell_screenshots/")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sell {self.crypto_amount} {self.crypto.upper()} by {self.user.email} ({self.status})"








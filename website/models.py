from django.db import models
from django.db import models
from customusers.models import CustomUser as User


class Purchase(models.Model):
    CONTACT_CHOICES = [
        ("email", "Email"),
        ("whatsapp", "WhatsApp"),
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} bought {self.crypto_amount} {self.crypto} via {self.contact_method}"

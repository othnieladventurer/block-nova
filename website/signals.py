from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Purchase
from .services import send_whatsapp_message

@receiver(post_save, sender=Purchase)
def purchase_created(sender, instance, created, **kwargs):
    if created and instance.contact_method == "whatsapp" and instance.whatsapp_number:
        message = (
            f"Hello {instance.user.email},\n\n"
            f"Your purchase of {instance.crypto_amount:.6f} {instance.crypto.upper()} "
            f"(${instance.total:.2f}) has been received.\n"
            "We will process your transaction within 30-55 minutes."
        )
        send_whatsapp_message(instance.whatsapp_number, message)

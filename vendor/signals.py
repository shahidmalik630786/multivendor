from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Vendor


@receiver(post_delete, sender=Vendor)
def delete_related_user(sender, instance, **kwargs):
    """Delete related CustomUser when Vendor is deleted."""
    if instance.user:
        instance.user.delete()
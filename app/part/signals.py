from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Part, Inventory


@receiver(post_save, sender=Part)
def update_inventory(sender, instance, created, **kwargs):
    """
    Bir parça (Part) eklendiğinde otomatik olarak envantere ekler veya miktarı artırır.
    """
    if created:
        inventory, created = Inventory.objects.get_or_create(
            part=instance, defaults={"quantity": 1}
        )
        if not created:
            inventory.quantity += 1
            inventory.save()

        print(
            f"Envanter Güncellendi: {instance.get_name_display()} - {inventory.quantity} adet"
        )

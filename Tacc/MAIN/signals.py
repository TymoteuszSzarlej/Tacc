from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .utils import log  # Importujemy funkcję logowania
from django.apps import apps  # Aby dynamicznie dostać się do modeli

@receiver(post_save)
def log_model_save(sender, instance, created, **kwargs):
    model_name = sender.__name__
    if created:
        log(f"Utworzono nową instancję: {model_name} (ID: {instance.pk})", "success")
    else:
        log(f"Zaktualizowano instancję: {model_name} (ID: {instance.pk})", "success")

@receiver(post_delete)
def log_model_delete(sender, instance, **kwargs):
    model_name = sender.__name__
    log(f"Usunięto instancję: {model_name} (ID: {instance.pk})", "success")

from django.dispatch import Signal
from django.models.signals import post_save
from django.conf import Settings
from .models import UserAccess


User = settings.AUTH_USER_MODEL

@post_save(sender=User)
def set_access_on_create(sender, instance, created, *args, **kwargs):
	if created:
		UserAccess.objects.create(user=instance, allowed=instance.is_superuser)
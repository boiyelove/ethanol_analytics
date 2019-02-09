from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel
# Create your models here.

class UserAccessRequest(TimeStampedModel):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='useraccess')
	is_allowed = models.NullBooleanField()
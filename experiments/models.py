from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel

User = settings.AUTH_USER_MODEL
EXPERIMENT_CHOICES = ((0,'created'), (1,'running'),(2,'completed'))
# Create your models here.
class Asset(TimeStampedModel):
	name = models.CharField(max_length=120)

class Experiment(TimeStampedModel):
	test_name = models.CharField(max_length=120)
	start_date = models.DateField()
	end_date = models.DateField()
	lookback_window = models.PositiveIntegerField()
	analysis_window = models.PositiveIntegerField()
	goal = models.CharField(max_length=120)
	additional_comments = models.TextField()
	assets = models.ManyToManyField(Asset)
	active_flag = models.BooleanField()
	status = models.PositiveIntegerField(default=0, choices=EXPERIMENT_CHOICES)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
	modified_by = models.ManyToManyField(User, related_name='editors')
from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel

User = settings.AUTH_USER_MODEL
EXPERIMENT_CHOICES = ((0,'created'), (1,'running'),(2,'completed'))
ACTIVEFLAG_CHOICES = ((0, 'inactive'), (1, 'active'))
# Create your models here.
class Asset(TimeStampedModel):
	name = models.CharField(max_length=120)

	def __str__(self):
		return self.name

class Experiment(TimeStampedModel):
	test_name = models.CharField(max_length=120)
	start_date = models.DateField()
	end_date = models.DateField()
	lookback_window = models.PositiveIntegerField()
	analysis_window = models.PositiveIntegerField()
	goal = models.CharField(max_length=120)
	additional_comments = models.TextField()
	assets = models.ManyToManyField(Asset)
	active_flag = models.PositiveIntegerField(default=1, choices=ACTIVEFLAG_CHOICES)
	status = models.PositiveIntegerField(default=0, choices=EXPERIMENT_CHOICES)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
	modified_by = models.ManyToManyField(User, related_name='editors')

	def __str__(self):
		return self.test_name

class Metric(TimeStampedModel):
	name = models.CharField(max_length=160)

	def __str__(sekf):
		return self.name

class AssetCategory(TimeStampedModel):
	name = models.CharField(max_length=160)

	def __str__(self):
		return self.name


from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel

User = settings.AUTH_USER_MODEL
EXPERIMENT_CHOICES = ((0,'created'), (1,'running'),(2,'completed'))
ACTIVEFLAG_CHOICES = ((0, 'inactive'), (1, 'active'))
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
	active_flag = models.PositiveIntegerField(default=1, choices=ACTIVEFLAG_CHOICES)
	status = models.PositiveIntegerField(default=0, choices=EXPERIMENT_CHOICES)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
	modified_by = models.ManyToManyField(User, related_name='editors')

class Metric(TimeStampedModel):
	name = models.CharField(max_length=160)

class AssetCategory(TimeStampedModel):
	name = models.CharField(max_length=160)

class ExperimentResult(TimeStampedModel):
	asset_category = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True)
	metric = models.ForeignKey(Metric, on_delete=models.SET_NULL, null=True)
	old_mean = models.FloatField()
	new_mean = models.FloatField()
	mean_difference = models.FloatField()
	pct_diff_mean = models.FloatField()
	agg_level = models.FloatField()
	sensor_id = models.FloatField()
	old_sd = models.FloatField()
	new_sd = models.FloatField()
	standard_dev_diff = models.FloatField()
	f_statistics = models.FloatField()
	p_value = models.FloatField()

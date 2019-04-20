from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.

class AnomalyData(TimeStampedModel):
	sensor_id = models.CharField(max_length=60)
	anomaly_start = models.DateTimeField()
	anomaly_end = models.DateTimeField()
	asset_category = models.CharField(max_length=60)
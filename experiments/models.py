from django.db import models, connections
from django.conf import settings
from model_utils.models import TimeStampedModel
from core.models import dictfetchall

User = settings.AUTH_USER_MODEL
EXPERIMENT_CHOICES = ((0,'created'), (1,'running'),(2,'completed'))
ACTIVEFLAG_CHOICES = ((0, 'inactive'), (1, 'active'))
# Create your models here.
class Asset(TimeStampedModel):
	name = models.CharField(max_length=120)

	def __str__(self):
		return self.name


def get_assets():
	with connections['sensors'].cursor() as cursor:
		cursor.execute("Select asset_category from whse.dim_sensor_metadata where asset_category != '' group by 1 order by 1;")
		return dictfetchall(cursor)

ASSET_CHOICES = tuple([(x['asset_category'],x['asset_category']) for x in get_assets()])

class Experiment(TimeStampedModel):
	test_name = models.CharField(max_length=120)
	change_date = models.DateTimeField()
	lookback_window = models.PositiveIntegerField()
	analysis_window = models.PositiveIntegerField()
	goal = models.CharField(max_length=120)
	additional_comments = models.TextField()
	assets = models.CharField(max_length=500)
	active_flag = models.PositiveIntegerField(default=1, choices=ACTIVEFLAG_CHOICES)
	status = models.PositiveIntegerField(default=0, choices=EXPERIMENT_CHOICES)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
	modified_by = models.ManyToManyField(User, related_name='editors')

	def __str__(self):
		return self.test_name

	def get_assets(self):
		return self.assets.split(',')

	def assets_from_list(data):
		self.assets = ','.join(data)
		return self

	def get_status(self):
		return EXPERIMENT_CHOICES[self.status][1]


	@staticmethod
	def get_numerical_data(sensor_id=None):
		with connections['sensors'].cursor() as cursor:
			if sensor_id:
				cursor.execute("Select sensor_id, sensor_description, value, time, (case when time > change_date then 'after' when time <= change_date then 'before' end)as group from ( Select b.sensor_id, sensor_description, change_date, lookback_window, analysis_window,a.asset_category,d.value,d.time from (Select id, change_date, lookback_window, analysis_window, unnest(assets) as asset_category from whse.dim_experimentation_metadata ) a inner join whse.dim_sensor_metadata b on a.asset_category = b.asset_category and sensor_id = '{}' inner join  whse.agg_hour_sensor_values d on b.sensor_id = d.sensor_id and d.time between change_date:: date - lookback_window and change_date:: date + analysis_window) k;".format(sensor_id))
			else:
				cursor.execute("Select sensor_id, sensor_description, value, time, (case when time > change_date then 'after' when time <= change_date then 'before' end)as group from ( Select b.sensor_id, sensor_description, change_date, lookback_window, analysis_window,a.asset_category,d.value,d.time from (Select id, change_date, lookback_window, analysis_window, unnest(assets) as asset_category from whse.dim_experimentation_metadata ) a inner join whse.dim_sensor_metadata b on a.asset_category = b.asset_category and sensor_id = 'PORT_CIP.AB_A.F44:41' inner join  whse.agg_hour_sensor_values d on b.sensor_id = d.sensor_id and d.time between change_date:: date - lookback_window and change_date:: date + analysis_window) k;")
				
			return dictfetchall(cursor)

		




class Metric(TimeStampedModel):
	name = models.CharField(max_length=160)

	def __str__(sekf):
		return self.name
class AssetCategory(TimeStampedModel):
	name = models.CharField(max_length=160)

	def __str__(self):
		return self.name





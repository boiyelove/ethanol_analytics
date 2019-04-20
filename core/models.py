from django.db import models, connections
from django.conf import settings
from model_utils.models import TimeStampedModel
# Create your models here.

class UserAccessRequest(TimeStampedModel):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='useraccess')
	is_allowed = models.NullBooleanField()



def dictfetchall(cursor):
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	]



class Sensor(TimeStampedModel):
	sensor_id = models.CharField(max_length=60, unique=True)
	show_on_dashboard = models.BooleanField(default=True)

def get_active_sensors():
	sensor_id = Sensor.objects.filter(show_on_dashboard=True).values_list('sensor_id', flat=True)
	sensor_id =   "'" +  "','".join(sensor_id)  + "'"
	print(sensor_id)
	return sensor_id


def get_sensor_data(n=31, sensor_id=None):
	with connections['sensors'].cursor() as cursor:
		cursor.execute("Select date, b.sensor_description, a.sensor_id,sensor_units, day_avg, week_avg, month_avg, day_pct_change, week_pct_change, month_pct_change , asset_category, asset_name from whse.agg_day_kpi a inner join whse.dim_sensor_metadata b on a.sensor_id = b.sensor_id and a.sensor_id in (%s) order by date desc limit %s" % (sensor_id, n))
		return dictfetchall(cursor)

def get_latest_data(sensor_id=None):
	n=8
	if not sensor_id:
		sensor_id = get_active_sensors()
	if sensor_id:
		n = len(sensor_id.split(','))
	with connections['sensors'].cursor() as cursor:
		cursor.execute("Select date, b.sensor_description, a.sensor_id,sensor_units, day_avg, week_avg, month_avg, day_pct_change, week_pct_change, month_pct_change , asset_category, asset_name from whse.agg_day_kpi a inner join whse.dim_sensor_metadata b on a.sensor_id = b.sensor_id and a.sensor_id in (%s) order by date desc limit %s" % (sensor_id, n))
		return dictfetchall(cursor)
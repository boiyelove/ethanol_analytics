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

def get_sensor_data(n=31, sensor_id="'PORT_CIP.AB_B.F44:111','PORT_CIP.AB_B.F44:110','PORT_CIP.AB_K.F44:70','PORT_CIP.AB_C.N15:203', 'PORT_CIP.AB_C.N15:223','PORT_CIP.AB_C.F44:130','PORT_CIP.AB_C.F44:120','PORT_CIP.AB_B.F44:50'"):
	with connections['sensors'].cursor() as cursor:
		cursor.execute("Select date, b.sensor_description, a.sensor_id,sensor_units, day_avg, week_avg, month_avg, day_pct_change, week_pct_change, month_pct_change , asset_category, asset_name from kpi_agg_table a inner join sensor_metadata b on a.sensor_id = b.sensor_id and a.sensor_id in (%s) order by date desc limit %s" % (sensor_id, n))
		return dictfetchall(cursor)

def get_latest_data(sensor_id="'PORT_CIP.AB_B.F44:111','PORT_CIP.AB_B.F44:110','PORT_CIP.AB_K.F44:70','PORT_CIP.AB_C.N15:203', 'PORT_CIP.AB_C.N15:223','PORT_CIP.AB_C.F44:130','PORT_CIP.AB_C.F44:120','PORT_CIP.AB_B.F44:50'"):
	with connections['sensors'].cursor() as cursor:
		cursor.execute("Select date, b.sensor_description, a.sensor_id,sensor_units, day_avg, week_avg, month_avg, day_pct_change, week_pct_change, month_pct_change , asset_category, asset_name from kpi_agg_table a inner join sensor_metadata b on a.sensor_id = b.sensor_id and a.sensor_id in (%s) order by date desc limit 8" % sensor_id)
		return dictfetchall(cursor)

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

def get_sensor_data(n=10, sensor_id="'PORT_CIP.AB_B.F44:111','PORT_CIP.AB_B.F44:110','PORT_CIP.AB_K.F44:70','PORT_CIP.AB_C.N15:203', 'PORT_CIP.AB_C.N15:223','PORT_CIP.AB_C.F44:130','PORT_CIP.AB_C.F44:120','PORT_CIP.AB_B.F44:50'"):
	with connections['sensors'].cursor() as cursor:
		cursor.execute("Select date, b.sensor_description, a.sensor_id,sensor_units, day_avg, week_avg, month_avg, day_pct_change, week_pct_change, month_pct_change , asset_category, asset_name from kpi_agg_table a inner join sensor_metadata b on a.sensor_id = b.sensor_id and a.sensor_id in (%s) order by date desc limit %s" % (sensor_id, n))
		return dictfetchall(cursor)


# class Sensor(models.Model):
# 	date = models.DateField()
# 	sensor_descrition = models.CharField(max_length=255, null=True)
# 	sensor_id = models.TextField(null=True)
# 	sensor_units =  models.CharField(max_length=255, null=True)
# 	day_avg = models.FloatField()
# 	week_avg = models.FloatField()
# 	month_avg = models.FloatField()
# 	day_pct_change = models.FloatField(default=0)
# 	week_pct_change = models.FloatField(default=0)
# 	month_pct_change = models.FloatField(default=0)
# 	asset_category = models.CharField(max_length=255, null=True)
# 	asset_name = models.CharField(max_length=255, null=True)

# Sensor.objects.raw("Select date,sensor_description, a.sensor_id,sensor_units, day_avg, week_avg, month_avg, day_pct_change, week_pct_change, month_pct_change , \
# 			asset_category, asset_name  \
# 			from kpi_agg_table a  \
# 			left join sensor_metadata b \
# 			on a.sensor_id = b.sensor_id \
# 			and a.sensor_id in  \
# 			('PORT_CIP.AB_B.F44:111','PORT_CIP.AB_B.F44:110','PORT_CIP.AB_K.F44:70','PORT_CIP.AB_C.N15:203', \
# 			'PORT_CIP.AB_C.N15:223','PORT_CIP.AB_C.F44:130','PORT_CIP.AB_C.F44:120','PORT_CIP.AB_B.F44:50') \
# 			order by date desc")

from django.db import connections
from core.models import dictfetchall
from model_utils.models import TimeStampedModel

# Create your models here.

class AnomalyData:
	# sensor_id = models.CharField(max_length=60)
	# anomaly_start = models.DateTimeField()
	# anomaly_end = models.DateTimeField()
	# asset_category = models.CharField(max_length=60)


	@staticmethod
	def get_anomaly_data(id=None):
		
		with connections['sensors'].cursor() as cursor:
			if id:
				cursor.execute("Select * from whse.dim_dash_app_metadata where (category = 'anomaly') AND (id = {0})".format(id))
				result =  cursor.fetchone()
				columns = [x.name for x in cursor.description]
				result = dict(zip(columns, result))
				return result
			else:
				cursor.execute("Select * from whse.dim_dash_app_metadata where category = 'anomaly'")
				return dictfetchall(cursor)


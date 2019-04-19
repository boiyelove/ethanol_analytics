from django.db import connections
from core.models import dictfetchall

# Create your models here.
def get_allsensors():
	with connections['sensors'].cursor() as cursor:
			cursor.execute("Select sensor_description,asset_category, asset_name, sensor_id from whse.dim_sensor_metadata order by asset_category desc, asset_name")
			return dictfetchall(cursor)

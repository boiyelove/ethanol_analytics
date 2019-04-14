from django.db import connections, models
from model_utils.models import TimeStampedModel
from core.models import dictfetchall
# Create your models here.
from .dashapps import board_readings1, board_readings2

def get_uploaddata(id=None):
	
	with connections['sensors'].cursor() as cursor:
		if id:
			cursor.execute("Select * from whse.dim_dash_app_metadata where (category = 'data_capture') AND (id = {0})".format(id))
			result =  cursor.fetchone()
			columns = [x.name for x in cursor.description]
			result = dict(zip(columns, result))
			return result
		else:
			cursor.execute("Select * from whse.dim_dash_app_metadata where category = 'data_capture' order by id")
			return dictfetchall(cursor)

class DataFileUpload(TimeStampedModel):
	csv_file = models.FileField(upload_to='uploaded/data_uploads')

class DataUpload(TimeStampedModel):
	description = models.CharField(max_length=60)
	value = models.CharField(max_length=60)


from django.db import connections
from model_utils import TimeStampedModel
from core.models import dictfetchall
# Create your models here.


def get__data(id=None):
	
	with connections['sensors'].cursor() as cursor:
		if id:
			cursor.execute("Select * from dash_app_metadata where category = 'data_capture') AND (where id = {0})".format(id))
			result =  cursor.fetchone()
			columns = [x.name for x in cursor.description]
			result = dict(zip(columns, result))
			return result
		else:
			cursor.execute("Select * from dash_app_metadata where category = 'data_capture'")
			return dictfetchall(cursor)

class DataFileUpload(TimeStampedModel):
	csv_file = models.FileField(upload_to='uploaded/data_uploads')

class DataUpload(TimeStampedModel):
	description = models.TextField()
	value = models.CharField(max_length=60)


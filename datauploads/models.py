from django.db import connections
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



from django.db import connections
from core.models import dictfetchall
# Create your models here.


def get_report_data():
	with connections['sensors'].cursor() as cursor:
		cursor.execute("Select * from dash_app_metadata")
		return dictfetchall(cursor)



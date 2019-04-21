from django import template
from anomaly_detection.models import AnomalyData

register = template.Library()

@register.simple_tag
def all_anomalydata():
	return AnomalyData.get_anomaly_data()
from django import template
from reports.models import get_report_data

register = template.Library()

@register.simple_tag
def all_reports():
	return get_report_data()
from django import template
from reports.models import get_report_data
import math

register = template.Library()

@register.simple_tag
def all_reports():
	return get_report_data()

@register.filter
def float2rep(num=None):
	if (num is None) or math.isnan(num):
		return '-'
	else:
		# if perc:
		# 	return "%.2f%%" % float(num)
		# else:
		return "%.2f" % float(num)
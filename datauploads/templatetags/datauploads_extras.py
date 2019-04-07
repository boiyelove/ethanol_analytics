from django import template
from datauploads.models import get_uploaddata
import math

register = template.Library()

@register.simple_tag
def all_datamethods():
	return get_uploaddata()
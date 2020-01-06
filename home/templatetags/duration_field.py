from django import template
import pdb
import time
import datetime
from datetime import timedelta
register = template.Library()


@register.filter(name='duration_field')
def duration(td):
	total_seconds = int(td.total_seconds())
	return time.strftime("%H:%M:%S",time.gmtime(total_seconds))

@register.filter(name='iduration_field')
def iduration(td):
	total_seconds = timedelta(microseconds=td).total_seconds()
	return time.strftime("%H:%M:%S",time.gmtime(total_seconds))
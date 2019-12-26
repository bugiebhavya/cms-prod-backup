from django import template
import pdb
import time
register = template.Library()


@register.filter(name='duration_field')
def duration(td):
	total_seconds = int(td.total_seconds())
	return time.strftime("%H:%M:%S",time.gmtime(total_seconds))
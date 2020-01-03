from django import template
import math
register = template.Library()
from django.utils.translation import ugettext_lazy as _

@register.filter(name='convert_size')
def convert_size(size_bytes):
	if size_bytes == 0:
		return "0B"
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return "%s %s" % (s, size_name[i])

@register.simple_tag(name='class_name')
def get_class_name(form):
	return "Add %s"%_(form.instance._meta.verbose_name)
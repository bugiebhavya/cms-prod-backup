from django.template import Library
from django.shortcuts import reverse
import pdb
from django.utils.safestring import mark_safe

register = Library()

@register.simple_tag()
def reverse_url(page, url_name, channel, base_url=''):
	if page.url:
		base_url = page.url
	try:
		url = base_url + page.reverse_subpage(url_name,args=[channel])
		return url
	except:
		return base_url

@register.filter(name="get_related_url")
def get_related_url(bound_field):
	if bound_field.field.__class__.__name__ == 'ModelChoiceField':
		ADD_URL = {
			'area': '/admin/documents/area/create/',
			'subject': '/admin/documents/subject/create/',
			'topic': '/admin/documents/topic/create/',
			'subtopic': '/admin/documents/subtopic/create/',
			'natures': '/admin/documents/natures/create/',
		}
		url = ADD_URL.get(bound_field.name, '')
		return mark_safe('<a class="related-widget-wrapper-link add-related" href="%s">+</a>'%url)
	return ''

@register.simple_tag()
def area_list():
	from modules.documents.models import Area
	return Area.objects.all()
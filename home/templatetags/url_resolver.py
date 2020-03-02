from django.template import Library
from django.shortcuts import reverse
import pdb
from django.utils.safestring import mark_safe

ADD_URL = {
			'area': '/admin/documents/area/create/',
			'subject': '/admin/documents/subject/create/',
			'topic': '/admin/documents/topic/create/',
			'subtopic': '/admin/documents/subtopic/create/',
			'nature': '/admin/documents/natures/create/',
			'collection': '/admin/collections/add/',
			'channel': '/admin/videos/channels/add/',
			'associate': '/admin/users/associate/create/',
			'sector': '/admin/users/associatesector/create/',
			'groups': '/admin/groups/new/',
			'associate_level': '/admin/users/associateslevel/create/'
		}

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
		
		url = ADD_URL.get(bound_field.name, '')
		return mark_safe('<a class="related-widget-wrapper-link add-related" href="%s?_popup=1">+</a>'%url)
	return ''

@register.simple_tag()
def area_list():
	from modules.documents.models import Area
	return Area.objects.all()

@register.filter(name='is_popup')
def is_popup(request):
	return request.GET.get('_popup', False)

@register.filter(name='can_add_related')
def can_add_related(bound_field):
	return bound_field.name in ADD_URL.keys()
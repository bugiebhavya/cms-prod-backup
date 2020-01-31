from django.template import Library
import pdb
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

@register.simple_tag()
def area_list():
	from modules.documents.models import Area
	return Area.objects.all()
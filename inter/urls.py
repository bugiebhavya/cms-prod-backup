from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from home import controller 
from search import views as search_views
from modules.documents.views import MediaDetailView

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^search/', search_views.search, name='search'),
    url('us-login', controller.LoginView.as_view(), name="us-login"), 
    url(r'^comment/$', controller.CommentView.as_view(), name="comment-view"),
    url('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    #url(r'^media/watch/(?P<pk>[0-9]+)', MediaDetailView.as_view()),
    url(r'', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

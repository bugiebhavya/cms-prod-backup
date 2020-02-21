from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from home import controller 
from search import views as search_views
from modules.documents.views import MediaDetailView, FilterCatalogsView, WatchVideoView, ReadDocumentView, ViewImageView
from modules.dashboard.notification import NotificationListView, RemoveNotificationView
from modules.users.views import FavAlterView
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^django-admin/', admin.site.urls),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^search/', search_views.search, name='search'),
    url(r'^medias/videos/(?P<media_id>[-\w]+)/', WatchVideoView.as_view(), name='video_detail'),
    url(r'^medias/document/(?P<media_id>[-\w]+)/', ReadDocumentView.as_view(), name='document_detail'),
    url(r'^medias/image/(?P<media_id>[-\w]+)/', ViewImageView.as_view(), name='image_detail'),

    url(r'^us-login/', controller.LoginView.as_view(), name="us-login"), 
    url(r'^comment/$', controller.CommentView.as_view(), name="comment-add"),
    url(r'^medias/fav/$', FavAlterView.as_view(), name='fav-alter'),
    url(r'^api/notifications/$', NotificationListView.as_view(), name='notifications'),
    url(r'^api/notifications/(?P<pk>[-\w]+)/remove$', RemoveNotificationView.as_view(), name='notifications'),
    url(r'^filter/catalogs/$', FilterCatalogsView.as_view(), name='filter-catalogs'),
    url(r'', include(wagtail_urls)),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

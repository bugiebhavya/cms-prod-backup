from django import forms
from django.db import models
from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
from django.shortcuts import render
import pdb 
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.documents.edit_handlers import DocumentChooserPanel

from modelcluster.fields import ParentalKey
from taggit.models import Tag as TaggitTag
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import (InlinePanel, MultiFieldPanel,FieldPanel,)

from wagtailvideos.models import Video
from wagtailvideos.edit_handlers import VideoChooserPanel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from wagtailvideos.models import Channels
from django.contrib import messages

class DashboardPageCarouselVideos(Orderable):
    '''Between 1 and 5 imagges for the home carousel '''
    page = ParentalKey("dashboard.DashboardPage", related_name="carousel_media")
    carousel_video = models.ForeignKey(
        "wagtailvideos.Video",
        null = True, 
        blank = True,
        on_delete= models.SET_NULL,
        related_name = "+" 
        )
    carousel_document = models.ForeignKey(
        "documents.CustomDocument",
        null = True, 
        blank = True,
        on_delete= models.SET_NULL,
        related_name = "+" 
        )


    panels = [
            VideoChooserPanel("carousel_video"),
            DocumentChooserPanel("carousel_document")
    ]


class MediaView(models.Model):
    class Meta:
        verbose_name = _('Media Views')
        verbose_name_plural = _('Media Views')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_('Content Type'))
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name=_('User'))
    object_id = models.PositiveIntegerField(verbose_name=_('Content ID'))
    content_object = GenericForeignKey('content_type', 'object_id')
    views = models.PositiveIntegerField(default=0, verbose_name=_('Total Views'), null=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.views)

    @property
    def iviews(self):
        print('-- %s'%self.views)
        if self.views:
            return self.views
        return 0
    

class DashboardPage(RoutablePageMixin, Page):
    template = 'dashboard/index.html'
    content_panels = Page.content_panels + [
            
            MultiFieldPanel([

                    InlinePanel("carousel_media", min_num=1, label="Media"),

                ], heading="Carousel Media"),

    ]

    @route(r'^profile/$', name="profile")
    def user_profile(self, request, *args, **kwargs):
        return render(request, 'dashboard/profile.html')

    @route(r'^history/$', name="history")
    def user_history(self, request, *args, **kwargs):
        medias=[]
        if request.user and request.user.is_authenticated:
            content_type_document = ContentType.objects.get(model='customdocument')
            content_type_video = ContentType.objects.get(model='video')
            videos = ContentType.objects.raw(f"SELECT vid.id, vid.title, vid.thumbnail, vid.created_at, vid.duration, mv.views, vid.author FROM dashboard_mediaview As mv LEFT OUTER JOIN wagtailvideos_video AS vid ON (mv.object_id = vid.id AND (mv.content_type_id = {content_type_video.id})) WHERE (mv.user_id = 1 AND vid.id IS NOT NULL)")
            documents = ContentType.objects.raw(f"SELECT dc.id, dc.title, dc.thumbnail, dc.created_at, dc.file_size, mv.views, dc.author FROM dashboard_mediaview As mv LEFT OUTER JOIN documents_customdocument AS dc ON (mv.object_id = dc.id AND (mv.content_type_id = {content_type_document.id})) WHERE (mv.user_id = 1 AND dc.id IS NOT NULL)")
            from itertools import chain
            media = list(chain(videos, documents))
            medias = sorted(media, key=lambda x: x.views, reverse=True)

        return render(request, 'dashboard/history.html', {'medias': medias})


    @route(r'^logout/$', name='user-logout')
    def logout(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Successfully logout, Please login.')
        return HttpResponseRedirect('/')


class ChannelPageCarouselVideos(Orderable):
    '''Between 1 and 5 imagges for the home carousel '''
    page = ParentalKey("dashboard.ChannelPage", related_name="channels")
    channel = models.ForeignKey(
        "wagtailvideos.Channels",
        null = True, 
        blank = False,
        on_delete= models.SET_NULL,
        related_name = "+" 
        )


    panels = [
            FieldPanel("channel")
    ]


class ChannelPage(RoutablePageMixin,Page):
    template = 'channel/index.html'
    

    content_panels = Page.content_panels + [
            
            MultiFieldPanel([

                    InlinePanel("channels", min_num=1, label="Channels"),

                ], heading="Channels"),

    ]
    
    @route(r'^(?P<channel>[-\w]+)/media/$', name="channel_details")
    def channel_details(self, request, *args, **kwargs):
        # try:
        def get_views(x):
            try:
                return x.media_views.last().views
            except:
                return 0

        channel = Channels.objects.get(id=kwargs.get('channel'))
        from itertools import chain
        media = list(chain(channel.documents.all(), channel.video_set.all()))
        media_list = sorted(media, key=lambda x: get_views(x), reverse=True)
        from home.models import ReferenceUrlPage
        homepage = ReferenceUrlPage(request)
        return render(request, 'channel/details.html', {'medias': media_list, 'channel': channel, 'homepage': homepage})
        # except Exception as ex:
        #     messages.info(request, str(ex))
        #     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


from django import forms
from django.db import models
from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
from django.shortcuts import render
import pdb 
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey
from taggit.models import Tag as TaggitTag
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import (InlinePanel, MultiFieldPanel,FieldPanel,)
from django.db.models.signals import post_save 
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
        on_delete= models.CASCADE,
        related_name = "+" 
        )
    carousel_document = models.ForeignKey(
        "documents.CustomDocument",
        null = True, 
        blank = True,
        on_delete= models.CASCADE,
        related_name = "+" 
        )

    carousel_image = models.ForeignKey(
        "documents.CustomImage",
        null = True, 
        blank = True,
        on_delete= models.CASCADE,
        related_name = "+" 
    )

    panels = [
            VideoChooserPanel("carousel_video"),
            DocumentChooserPanel("carousel_document"),
            ImageChooserPanel("carousel_image")
    ]


class MediaView(models.Model):
    class Meta:
        verbose_name = _('Media Views')
        verbose_name_plural = _('Media Views')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_('Content Type'))
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name=_('User'), null=True, blank=True)
    object_id = models.PositiveIntegerField(verbose_name=_('Content ID'))
    content_object = GenericForeignKey('content_type', 'object_id')
    views = models.PositiveIntegerField(default=1, verbose_name=_('Total Views'), null=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.views)

    @property
    def iviews(self):
        if self.views:
            return self.views
        return 0

class Notifications(models.Model):
    class Meta:
        verbose_name = _('Notifications')
        verbose_name_plural = _('Notifications')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_('Content Type'))
    seen_users = models.ManyToManyField(to="users.User", verbose_name=_('Seen Users'), null=True, blank=True)
    object_id = models.PositiveIntegerField(verbose_name=_('Content ID'))
    content_object = GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


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
        if request.user and request.user.is_authenticated:
            from modules.dashboard.models import MediaView
            medias = MediaView.objects.filter(user=request.user).distinct('object_id')
            return render(request, 'dashboard/history.html', {'medias': medias})
        return HttpResponseRedirect('/')

    @route(r'^favorites/$', name="favorites")
    def favorites(self, request, *args, **kwargs):
        from modules.users.models import Favorite
        favorites = Favorite.objects.filter(user=request.user).distinct()
        return render(request, 'fav/list.html', {'favorites': favorites})


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
        on_delete= models.CASCADE,
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
        try:
            def get_views(x):
                try:
                    return x.media_views.last().views
                except:
                    return 0

            channel = Channels.objects.get(id=kwargs.get('channel'))
            from itertools import chain
            media = list(chain(channel.documents.all(), channel.video_set.all(), channel.images.all()))
            media_list = sorted(media, key=lambda x: get_views(x), reverse=True)
            from home.models import ReferenceUrlPage
            homepage = ReferenceUrlPage(request)
            return render(request, 'channel/details.html', {'medias': media_list, 'channel': channel, 'homepage': homepage})
        except Exception as ex:
            messages.info(request, str(ex))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def dashboard_notification(sender, instance, **kwargs):
    try:
        if not instance.carousel_video.notifications.exists():
            Notifications.objects.create(content_object=instance.carousel_video)
        if not instance.carousel_document.notifications.exists():
            Notifications.objects.create(content_object=instance.carousel_document)
        if not instance.carousel_image.notifications.exists():
            Notifications.objects.create(content_object=instance.carousel_image)
    except Exception as ex:
        print(ex)

post_save.connect(dashboard_notification, sender=DashboardPageCarouselVideos)
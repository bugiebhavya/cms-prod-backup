from django import forms
from django.db import models
from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
from django.shortcuts import render
import pdb 
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
        return render(request, 'dashboard/history.html')


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
    


class MediaView(models.Model):
    class Meta:
        verbose_name = _('Media Views')
        verbose_name_plural = _('Media Views')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_('Content Type'))
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
    
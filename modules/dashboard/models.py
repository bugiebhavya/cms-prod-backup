from django import forms
from django.db import models
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
from django.shortcuts import render
import wagtail
import pdb 
from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel,
                                         InlinePanel, MultiFieldPanel,
                                         PageChooserPanel, StreamFieldPanel)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Orderable
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.snippets.models import register_snippet

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag as TaggitTag
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel,
)

from wagtailvideos.models import Video
from wagtailvideos.edit_handlers import VideoChooserPanel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from wagtailvideos.models import Channels
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

class DashboardPageCarouselVideos(Orderable):
    '''Between 1 and 5 imagges for the home carousel '''
    page = ParentalKey("dashboard.DashboardPage", related_name="carousel_videos")
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

                    InlinePanel("carousel_videos", min_num=1, label="Video"),

                ], heading="Carousel Videos"),

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
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    views = models.IntegerField()
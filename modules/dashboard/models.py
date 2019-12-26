from django import forms
from django.db import models
from django.http import Http404, HttpResponse
from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
from django.shortcuts import render
import wagtail
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


class DashboardPageCarouselVideos(Orderable):
    '''Between 1 and 5 imagges for the home carousel '''
    page = ParentalKey("dashboard.DashboardPage", related_name="carousel_videos")
    carousel_video = models.ForeignKey(
        "wagtailvideos.Video",
        null = True, 
        blank = False,
        on_delete= models.SET_NULL,
        related_name = "+" 
        )


    panels = [
            VideoChooserPanel("carousel_video")
    ]

class DashboardPage(RoutablePageMixin, Page):
    template = 'dashboard/index.html'
    content_panels = Page.content_panels + [
            
            MultiFieldPanel([

                    InlinePanel("carousel_videos", min_num=1, label="Video"),

                ], heading="Carousel Videos"),

    ]
    # def get_context(self, request, *args, **kwargs):
    #     context = super(DashboardPage, self).get_context(request, *args, **kwargs)
    #     context['videos'] = self.get_videos()
    #     return context

    def get_videos(self):
        self.videos = Video.objects.all()
        return self.videos

    
from django.contrib import admin
from .models import MediaView
from wagtail.contrib.modeladmin.options import (modeladmin_register, ModelAdmin,)

class MediaViewAdmin(ModelAdmin):
    """MediaViewAdmin admin."""

    model = MediaView
    menu_label = "MediaView"
    menu_icon = "placeholder"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("content_object", "views",)
    search_fields = ("content_object", "views",)

modeladmin_register(MediaViewAdmin) 
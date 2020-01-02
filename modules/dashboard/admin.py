from django.contrib import admin
from .models import MediaView
from wagtail.contrib.modeladmin.options import (modeladmin_register, ModelAdmin,)
from wagtail.contrib.modeladmin.helpers import PermissionHelper

from django.contrib import admin

from taggit.models import Tag, TaggedItem

class TagAdmin(ModelAdmin):
    model = Tag
    menu_label = 'Keyword'
    list_display = ["name", "slug"]
    ordering = ["name", "slug"]
    search_fields = ["name"]
    form_fields_exclude = ["slug"]
    menu_icon = "tag"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False

class ModelPermissionHelper(PermissionHelper):
    def user_can_create(self, user):
        return False

    def user_can_edit_obj(self, request, obj):
    	return False

class MediaViewAdmin(ModelAdmin):
    """MediaViewAdmin admin."""

    model = MediaView
    menu_icon = "view"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("content_object", "content_type", "object_id", "views",)
    permission_helper_class = ModelPermissionHelper

modeladmin_register(MediaViewAdmin) 
modeladmin_register(TagAdmin) 
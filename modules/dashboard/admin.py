from django.contrib import admin
from .models import MediaView
from wagtail.contrib.modeladmin.options import (modeladmin_register, ModelAdmin,)
from wagtail.contrib.modeladmin.helpers import PermissionHelper

from django.contrib import admin

from taggit.models import Tag, TaggedItem

class TagViewAdmin(ModelAdmin):
    create_template_name = 'wagtailadmin/common_template/create.html'
    edit_template_name = 'wagtailadmin/common_template/edit.html'
    model = Tag
    menu_icon = 'tag'
    menu_order = 290
    # add_to_settings_menu = True
    list_display = ("name", "id",)

modeladmin_register(TagViewAdmin)


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

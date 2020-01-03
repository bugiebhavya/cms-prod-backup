from django.contrib import admin
from .models import *
from wagtail.contrib.modeladmin.options import (modeladmin_register, ModelAdmin,)
from wagtail.contrib.modeladmin.helpers import PermissionHelper

class ModelPermissionHelper(PermissionHelper):
    def user_can_create(self, user):
        return False

    def user_can_edit_obj(self, request, obj):
    	return False

class AreaViewAdmin(ModelAdmin):
    model = Area
    menu_icon = "group"
    menu_order = 290
    add_to_settings_menu = True
    exclude_from_explorer = False
    list_display = ("name", "id", "created",)

modeladmin_register(AreaViewAdmin)

class SubjectViewAdmin(ModelAdmin):
    model = Subject
    menu_icon = "group"
    menu_order = 290
    add_to_settings_menu = True
    exclude_from_explorer = False
    list_display = ("name", "id", "created",)

modeladmin_register(SubjectViewAdmin)

class TopicViewAdmin(ModelAdmin):
    model = Topic
    menu_icon = "group"
    menu_order = 290
    add_to_settings_menu = True
    exclude_from_explorer = False
    list_display = ("name", "id", "created",)

modeladmin_register(TopicViewAdmin)

class SubTopicViewAdmin(ModelAdmin):
    model = SubTopic
    menu_icon = "group"
    menu_order = 290
    add_to_settings_menu = True
    exclude_from_explorer = False
    list_display = ("name", "id", "created",)

modeladmin_register(SubTopicViewAdmin)

class NaturesViewAdmin(ModelAdmin):
    model = Natures
    menu_icon = "group"
    menu_order = 290
    add_to_settings_menu = True
    exclude_from_explorer = False
    list_display = ("name", "id", "created",)

modeladmin_register(NaturesViewAdmin) 

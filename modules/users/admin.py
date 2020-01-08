from django.contrib import admin
from .models import AssociatesLevel, Associate
from wagtail.contrib.modeladmin.options import (modeladmin_register, ModelAdmin,)
from wagtail.contrib.modeladmin.helpers import PermissionHelper

from django.contrib import admin

from taggit.models import Tag, TaggedItem

class AssociatesLevelAdmin(ModelAdmin):
    create_template_name = 'wagtailadmin/common_template/create.html'
    edit_template_name = 'wagtailadmin/common_template/edit.html'
    model = AssociatesLevel
    menu_icon = "user"
    menu_order = 290
    add_to_settings_menu = True
    list_display = ("title", "allowed_users", "id","updated",)

modeladmin_register(AssociatesLevelAdmin)



class AssociatesAdmin(ModelAdmin):
    create_template_name = 'wagtailadmin/common_template/create.html'
    edit_template_name = 'wagtailadmin/common_template/edit.html'
    model = Associate
    menu_icon = "user"
    menu_order = 290
    add_to_settings_menu = True
    list_display = ("email","rfc", "email", "associate_level","updated",)

modeladmin_register(AssociatesAdmin)
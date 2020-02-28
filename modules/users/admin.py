from django.contrib import admin
from .models import AssociatesLevel, Associate, User, AssociateSector
from wagtail.contrib.modeladmin.options import (modeladmin_register, ModelAdmin,)
from wagtail.contrib.modeladmin.helpers import PermissionHelper
import pdb
from django.utils.translation import ugettext_lazy as _
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

class AssociateSectorAdmin(ModelAdmin):
    model = AssociateSector
    menu_icon = 'snippet'
    create_template_name = 'wagtailadmin/common_template/create.html'
    edit_template_name = 'wagtailadmin/common_template/edit.html'
    add_to_settings_menu = True
    list_display = ("value","notes","updated",)

modeladmin_register(AssociateSectorAdmin)
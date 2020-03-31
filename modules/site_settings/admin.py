from django.contrib import admin
from .models import *
from wagtail.contrib.modeladmin.options import (modeladmin_register, ModelAdmin,)
from wagtail.contrib.modeladmin.helpers import PermissionHelper


class GeneralParamsViewAdmin(ModelAdmin):
    create_template_name = 'wagtailadmin/common_template/create.html'
    edit_template_name = 'wagtailadmin/common_template/edit.html'
    model = GeneralParams
    menu_icon = "cogs"
    menu_order = 290
    list_display = ("key", "value", "created",)

modeladmin_register(GeneralParamsViewAdmin)
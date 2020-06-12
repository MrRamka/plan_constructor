from django.contrib import admin

# Core
from core.models import Color, UserColor, Plan


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'hex', 'type', 'author']


@admin.register(UserColor)
class CustomColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'hex', 'color_author']


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['author', 'name', 'type', 'version', 'date_creation', 'last_update']

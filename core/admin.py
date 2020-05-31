from django.contrib import admin

# Core
from core.models import Color, UserColor, Plan

admin.site.register(Color)
admin.site.register(UserColor)


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['author', 'name', 'type', 'version', 'date_creation']


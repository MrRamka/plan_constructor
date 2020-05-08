from django.contrib import admin

# Core
from core.models import Color, UserColor, Plan

admin.site.register(Color)
admin.site.register(UserColor)


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['plan_author', 'plan_name', 'plan_type', 'plan_version', 'plan_date_creation']

from django.urls import path

from core.views import HomeView, CreatePlanView, SettingsView, AddColorView

app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create/', CreatePlanView.as_view(), name='create_plan'),
    path('settings/', SettingsView.as_view(), name='settings'),

    # ajax
    path('add-color/', AddColorView.as_view(), name='add_color'),
]

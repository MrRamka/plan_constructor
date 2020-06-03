from django.urls import path

from core.views import HomeView, CreatePlanView

app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create/', CreatePlanView.as_view(), name='create_plan')
]

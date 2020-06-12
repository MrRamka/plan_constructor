from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from table.views import TableListView, TableDetailView

app_name = 'table'
urlpatterns = [
    path('list/', TableListView.as_view(), name='to_user_table_list'),
    path('test/', TemplateView.as_view(template_name='table/test.html')),
    path('<hash>/', TableDetailView.as_view(), name='to_plan')
]

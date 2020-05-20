from django.conf.urls import url
from django.urls import path

from table.views import TableListView, TableDetailView

app_name = 'table'
urlpatterns = [
    path('list/', TableListView.as_view(), name='to_user_table_list'),
    path('<hash>/', TableDetailView.as_view(), name='to_plan')
]

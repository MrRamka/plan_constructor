from django.conf.urls import url

from table.views import TableListView

app_name = 'table'
urlpatterns = [
    url('user-list/', TableListView.as_view(), name='to_user_table_list'),

]

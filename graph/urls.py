from django.conf.urls import url
from django.urls import path

from graph.views import GraphListView, GraphDetailView

app_name = 'graph'
urlpatterns = [
    path('list/', GraphListView.as_view(), name='to_user_graph_list'),
    path('<hash>/', GraphDetailView.as_view(), name='to_plan')
]

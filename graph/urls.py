from django.conf.urls import url

from graph.views import GraphListView, GraphDetailView

app_name = 'graph'
urlpatterns = [
    url('list/', GraphListView.as_view(), name='to_user_graph_list'),
    url('<hash>/', GraphDetailView.as_view(), name='to_plan')

]

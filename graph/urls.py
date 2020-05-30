from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from graph import apiview
from graph.views import GraphListView, GraphDetailView, AddNode, ChangeNodeLabel, ChangeNodePriority, DeleteEdge, \
    UpdateColor, DeleteNode, AddEdge

app_name = 'graph'
# Rest Api
router = routers.DefaultRouter()
router.register(r'vertices', apiview.VertexViewSet, basename='vertices_api')
router.register(r'edges', apiview.EdgeViewSet, basename='edges_api')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Start ajax
    # path('node/', NodeView.as_view(), name='node'),
    path('add-node/', AddNode.as_view(), name='add_node'),
    path('add-edge/', AddEdge.as_view(), name='add_edge'),

    path('update-label/', ChangeNodeLabel.as_view(), name='update_label'),
    path('update-priority/', ChangeNodePriority.as_view(), name='update_priority'),
    path('delete-edge/', DeleteEdge.as_view(), name='delete_edge'),
    path('update-color/', UpdateColor.as_view(), name='update_color'),
    path('delete-node/', DeleteNode.as_view(), name='delete_node'),

    # End ajax
    path('list/', GraphListView.as_view(), name='to_user_graph_list'),
    path('<hash>/', GraphDetailView.as_view(), name='to_plan'),
]

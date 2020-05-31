from rest_framework import viewsets
from rest_framework import permissions

from graph.models import Edge, Vertex
from graph.serializers import EdgeSerializer, VertexSerializer


class EdgeViewSet(viewsets.ModelViewSet):
    serializer_class = EdgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Edge.objects.filter(start_vertex__related_plan__author=user)


class VertexViewSet(viewsets.ModelViewSet):
    serializer_class = VertexSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Vertex.objects.filter(related_plan__author=user)

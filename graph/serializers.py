from rest_framework import serializers

from core.serializers import ColorSerializer
from graph.models import Vertex, Edge


class VertexSerializer(serializers.ModelSerializer):
    color = ColorSerializer(required=True)

    class Meta:
        model = Vertex
        fields = ('name', 'color', 'related_plan', 'priority')


class EdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edge
        fields = '__all__'

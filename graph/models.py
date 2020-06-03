from django.db import models

from core.models import PlanObject


class Vertex(PlanObject):
    """
    Representing graph vertex
    """
    pass


class Edge(models.Model):
    """
    Representing connection between vertex
    """
    # new id, library require hash id
    library_id = models.CharField(max_length=200, )
    start_vertex = models.ForeignKey(Vertex, on_delete=models.CASCADE, related_name='start_vertex')
    end_vertex = models.ForeignKey(Vertex, on_delete=models.CASCADE, related_name='end_vertex')

    def __str__(self):
        return f'{self.start_vertex.__str__()} - {self.end_vertex.__str__()}'

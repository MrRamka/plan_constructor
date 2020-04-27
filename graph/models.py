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
    start_vertex = models.ForeignKey(Vertex, on_delete=models.CASCADE)
    end_vertex = models.ForeignKey(Vertex, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.start_vertex.__str__()} - {self.end_vertex.__str__()}'

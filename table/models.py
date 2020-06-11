from django.db import models

from core.models import PlanObject, Plan


class Column(models.Model):
    """
    Table column model
    """
    related_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    column_position = models.PositiveIntegerField()
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.related_plan.__str__()} Position: {self.column_position}'


class Cell(PlanObject):
    """
    Representing graph vertex
    """
    start_column_position = models.ForeignKey(Column, on_delete=models.CASCADE)
    cell_duration = models.PositiveIntegerField()

    def __str__(self):
        return f'Start position: {self.start_column_position.__str__()} Duration: {self.cell_duration}'

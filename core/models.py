from django.db import models


class Color(models.Model):
    """
    Base color model
    """
    # String color in hex
    color_hex = models.CharField(max_length=6)
    color_name = models.CharField(max_length=20)
    color_description = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('color_name',)

    def __str__(self):
        return f'{self.color_name} (#{self.color_hex})'


class UserColor(Color):
    """
    Model of custom user colors
    """
    pass
    # color_author = models.ForeignKey(User, on_delete=models.CASCADE)
    #
    # def __str__(self):
    #     return f'{self.color_author.__str__()} - {super().__str__()}'


class GraphPlanManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(plan_type=Plan.GRAPH_TYPE)


class TablePlanManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(plan_type=Plan.TABLE_TYPE)


class Plan(models.Model):
    """
    Model base plan object
    """
    GRAPH_TYPE = 0
    TABLE_TYPE = 1
    TYPES = (
        (GRAPH_TYPE, 'Graph view of plan'),
        (TABLE_TYPE, 'Table view of plan')
    )

    plan_name = models.CharField(max_length=140)
    plan_slug = models.SlugField(max_length=140, db_index=True)
    plan_description = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    plan_version = models.PositiveSmallIntegerField()
    plan_type = models.PositiveIntegerField(
        choices=TYPES
    )
    plan_date_creation = models.DateTimeField(auto_now_add=True)
    # plan_author = models.ForeignKey(User, on_delete=models.CASCADE)

    # Managers
    table_plan_objects = TablePlanManager()
    graph_plan_objects = GraphPlanManager()

    # def __str__(self):
    #     return f'{self.user.__str__()} - {self.plan_name} ({self.plan_version})'

    class Meta:
        unique_together = ('plan_author', 'plan_slug', 'plan_version')
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'


class PlanObject(models.Model):
    """
    Abstract plan object model
    """
    plan_object_name = models.CharField(max_length=50)
    plan_object_color = models.ForeignKey(Color, on_delete=models.CASCADE)
    related_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    plan_object_priority = models.PositiveIntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.related_plan.plan_type} - {self.plan_object_name}'

import hashlib

from django.db import models
from django.db.models.manager import BaseManager, Manager
from django.urls import reverse
from django.utils.text import slugify

from user.models import User


class BaseColorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=Color.BASE_COLOR)


class UserColorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=Color.CUSTOM_COLOR)


class Color(models.Model):
    """
    Base color model
    """
    BASE_COLOR = 0
    CUSTOM_COLOR = 1
    TYPES = (
        (BASE_COLOR, 'Base color'),
        (CUSTOM_COLOR, 'User color')
    )
    type = models.PositiveIntegerField(
        choices=TYPES
    )
    # String color in hex
    hex = models.CharField(max_length=6)
    name = models.CharField(max_length=20)
    description = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # color manages
    objects = Manager()
    base_colors = BaseColorManager()
    custom_color = UserColorManager()

    def __str__(self):
        return f'{self.author.__str__()} - {super().__str__()}'

    class Meta:
        ordering = ('name',)


class UserColor(Color):
    """
    Model of custom user colors
    """
    # cant use inheritance because django create 1 to 1 field
    color_author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.color_author.__str__()} - {super().__str__()}'


class GraphPlanManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=Plan.GRAPH_TYPE)


class TablePlanManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=Plan.TABLE_TYPE)


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

    name = models.CharField(max_length=140)
    slug = models.SlugField(
        max_length=140,
        db_index=True,
        null=True,
        blank=True
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    version = models.PositiveSmallIntegerField()
    type = models.PositiveIntegerField(
        choices=TYPES
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)

    # Managers
    objects = Manager()
    graph_plan_objects = GraphPlanManager()
    table_plan_objects = TablePlanManager()

    def __str__(self):
        return f'{self.author.__str__()} - {self.name} ({self.version})'

    def save(self, *args, **kwargs):
        self.slug = hashlib.md5(
            (self.name + self.author.get_full_name() + str(self.version)).encode()).hexdigest()
        super(Plan, self).save(*args, **kwargs)

    def get_absolute_url(self):
        if self.type == self.GRAPH_TYPE:
            return reverse('graph:to_plan', args=(self.slug,))
        else:
            return reverse('table:to_plan', args=(self.slug,))

    class Meta:
        unique_together = ('author', 'slug', 'version')
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'


class PlanObject(models.Model):
    """
    Abstract plan object model
    """
    name = models.CharField(max_length=50)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    related_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    priority = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.related_plan.type} - {self.name}'

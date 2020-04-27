from django.contrib import admin

# Register your models here.
from graph.models import Vertex, Edge

admin.site.register(Vertex)
admin.site.register(Edge)
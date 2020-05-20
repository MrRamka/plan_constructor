import json
from functools import reduce
from operator import or_

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView

from core.models import Plan, Color
from graph.models import Vertex, Edge


class GraphListView(ListView, LoginRequiredMixin):
    model = Plan
    template_name = 'graph/graph_list.html'

    def get_queryset(self):
        return Plan.graph_plan_objects.filter(author=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['plan_type_graph'] = True
        context_data['plan_type'] = 'Graph plans'
        return context_data


class GraphDetailView(DetailView, LoginRequiredMixin):
    model = Plan
    template_name = 'graph/graph_detail.html'

    def get_object(self, queryset=None):
        return Plan.graph_plan_objects.get(slug=self.kwargs['hash'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['plan_type_graph'] = True

        # Add vertex
        vertices = Vertex.objects.filter(related_plan=self.get_object())
        context_data['vertices'] = vertices

        # Add edges
        edges = Edge.objects.filter(
            reduce(or_, [(Q(start_vertex=vertex) | Q(end_vertex=vertex)) for vertex in vertices])
        ).distinct()
        context_data['edges'] = edges

        # Add colors
        colors = Color.objects.all()
        context_data['colors'] = colors
        return context_data


class AddNode(LoginRequiredMixin, View):
    def post(self, request):
        if request.is_ajax():
            plan_id = request.POST.get('plan_id', None)

            vertex = Vertex.objects.create(
                name='Node name',
                color=Color.objects.get(id=1),
                related_plan=Plan.objects.get(id=plan_id)
            )

            data = {
                'v_name': vertex.name,
                'v_id': vertex.id,
                'v_color': vertex.color.hex,
                'v_priority': vertex.priority
            }

            return HttpResponse(json.dumps(data), content_type='application/json')

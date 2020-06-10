import json
from functools import reduce
from operator import or_

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from core.models import Plan, Color, UserColor
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


class GraphDetailView(LoginRequiredMixin, DetailView):
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
        if vertices:
            edges = Edge.objects.filter(
                reduce(or_, [(Q(start_vertex=vertex) | Q(end_vertex=vertex)) for vertex in vertices])
            ).distinct()
            context_data['edges'] = edges
        # custom color
        custom_colors = Color.custom_color.filter(author=self.request.user)
        context_data['custom_colors'] = custom_colors
        # Add colors
        colors = Color.base_colors.all()
        context_data['colors'] = colors

        return context_data


# todo  create mixin: allow edit only own components
class AddNode(LoginRequiredMixin, View):
    def post(self, request):
        if request.is_ajax():
            plan_id = request.POST.get('plan_id', None)

            vertex = Vertex.objects.create(
                name='Node name',
                color=Color.objects.get(id=1),
                related_plan=Plan.objects.get(id=plan_id)
            )
            # update last modified
            plan = Plan.objects.get(id=plan_id)
            plan.save()

            data = {
                'v_name': vertex.name,
                'v_id': vertex.id,
                'v_color': vertex.color.hex,
                'v_priority': vertex.priority
            }

            return HttpResponse(json.dumps(data), content_type='application/json')


class ChangeNodeLabel(LoginRequiredMixin, View):
    def post(self, request):
        if request.is_ajax():
            plan_id = request.POST.get('plan_id', None)
            node_id = request.POST.get('node_id', None)
            node_label = request.POST.get('new_node_name', None)
            node = Vertex.objects.get(id=node_id)
            node.name = node_label
            node.save()

            # update last modified
            plan = Plan.objects.get(id=plan_id)
            plan.save()

            data = {
                'status': 'OK'
            }

            return HttpResponse(json.dumps(data), content_type='application/json')


class ChangeNodePriority(LoginRequiredMixin, View):
    def post(self, request):
        if request.is_ajax():
            plan_id = request.POST.get('plan_id', None)
            node_id = request.POST.get('node_id', None)
            new_node_priority = request.POST.get('new_node_priority', None)
            node = Vertex.objects.get(id=node_id)
            node.priority = new_node_priority
            node.save()

            # update last modified
            plan = Plan.objects.get(id=plan_id)
            plan.save()

            data = {
                'status': 'OK'
            }
            return HttpResponse(json.dumps(data), content_type='application/json')


class AddEdge(LoginRequiredMixin, View):
    def post(self, request):
        if request.is_ajax():
            plan_id = request.POST.get('plan_id', None)
            node_start = request.POST.get('node_start', None)
            node_end = request.POST.get('node_end', None)
            node_hash = request.POST.get('node_hash', None)

            edge = Edge.objects.create(start_vertex_id=node_start, end_vertex_id=node_end, library_id=node_hash)

            # update last modified
            plan = Plan.objects.get(id=plan_id)
            plan.save()

            data = {
                'status': 'CREATED',
                'edge_id': edge.id
            }
            return HttpResponse(json.dumps(data), content_type='application/json')


class DeleteEdge(LoginRequiredMixin, View):
    def post(self, request):
        if request.is_ajax():
            plan_id = request.POST.get('plan_id', None)
            edge_id = request.POST.get('edge_id', None)
            edge = Edge.objects.get(library_id=edge_id)
            edge.delete()

            # update last modified
            plan = Plan.objects.get(id=plan_id)
            plan.save()

            data = {
                'status': 'DELETED'
            }
            return HttpResponse(json.dumps(data), content_type='application/json')


class UpdateColor(LoginRequiredMixin, View):
    def post(self, request):
        if request.is_ajax():
            plan_id = request.POST.get('plan_id', None)
            node_id = request.POST.get('node_id', None)
            new_node_color = request.POST.get('new_node_color', None)
            node = Vertex.objects.get(id=node_id)
            color = Color.objects.get(hex=new_node_color)
            node.color = color
            node.save()

            # update last modified
            plan = Plan.objects.get(id=plan_id)
            plan.save()
            data = {
                'status': 'OK'
            }
            return HttpResponse(json.dumps(data), content_type='application/json')


class DeleteNode(LoginRequiredMixin, View):
    def post(self, request):
        if request.is_ajax():
            plan_id = request.POST.get('plan_id', None)
            node_id = request.POST.get('node_id', None)
            node = Vertex.objects.get(id=node_id)
            node.delete()

            # update last modified
            plan = Plan.objects.get(id=plan_id)
            plan.save()

            data = {
                'status': 'DELETED'
            }
            return HttpResponse(json.dumps(data), content_type='application/json')

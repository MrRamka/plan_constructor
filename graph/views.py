from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from core.models import Plan


class GraphListView(ListView, LoginRequiredMixin):
    model = Plan
    template_name = 'graph/graph_list.html'

    def get_queryset(self):
        return Plan.graph_plan_objects.filter(plan_author=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['plan_type_graph'] = True
        context_data['plan_type'] = 'Graph plans'
        return context_data


class GraphDetailView(DetailView, LoginRequiredMixin):
    model = Plan
    template_name = 'graph/graph_detail.html'

    def get_object(self, queryset=None):
        return Plan.graph_plan_objects.get(plan_slug=self.kwargs['hash'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['plan_type_graph'] = True

        return context_data

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from core.models import Plan


class TableListView(ListView, LoginRequiredMixin):
    model = Plan
    template_name = 'table/table_list.html'

    def get_queryset(self):
        return Plan.table_plan_objects.filter(author=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # Hover navigation item
        context_data['plan_type_table'] = True
        # Plan type header
        context_data['plan_type'] = 'Table plans'
        return context_data


class TableDetailView(DetailView, LoginRequiredMixin):
    model = Plan
    template_name = 'table/table_detail.html'

    def get_object(self, queryset=None):
        return Plan.table_plan_objects.get(plan_slug=self.kwargs['hash'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # Hover navigation item
        context_data['plan_type_table'] = True

        return context_data

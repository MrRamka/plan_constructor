from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from core.models import Plan


class TableListView(ListView, LoginRequiredMixin):
    model = Plan
    template_name = 'table/table_list.html'

    def get_queryset(self):
        return Plan.table_plan_objects.filter(plan_author=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['plan_type_table'] = True
        context_data['plan_type'] = 'Table plans'
        return context_data

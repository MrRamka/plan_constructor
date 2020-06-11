from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from core.models import Plan, Color
from table.models import Column, Cell


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
        return Plan.table_plan_objects.get(slug=self.kwargs['hash'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # Hover navigation item
        context_data['plan_type_table'] = True

        # columns
        columns = Column.objects.filter(related_plan=self.get_object())
        context_data['columns'] = columns
        context_data['columns_amount'] = len(columns)

        # cells
        if columns:
            cells = Cell.objects.filter(related_plan=self.get_object())
            context_data['cells'] = cells

        # custom color
        custom_colors = Color.custom_color.filter(author=self.request.user)
        context_data['custom_colors'] = custom_colors
        # Add colors
        colors = Color.base_colors.all()
        context_data['colors'] = colors

        return context_data

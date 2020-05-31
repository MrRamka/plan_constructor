from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['plan_type_all'] = True
        context_data['plan_type'] = 'All plans'
        return context_data

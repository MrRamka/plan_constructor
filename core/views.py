from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView

from core.forms import CreatePlanForm
from core.models import Plan


class HomeView(LoginRequiredMixin, TemplateView):
    """
    Main page with all main information
    """
    template_name = 'core/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['plan_type_all'] = True
        context_data['plan_type'] = 'All plans'
        return context_data


class CreatePlanView(LoginRequiredMixin, CreateView):
    """
    Create plan view and redirect according plan type
    """
    form_class = CreatePlanForm
    template_name = 'core/create_plan.html'
    model = Plan
    success_url = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['create_plan'] = True
        return context_data

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            # Add user author
            plan = form.save(commit=False)
            plan.author = self.request.user
            plan.save()

            # change success_url according plan type
            plan_type = form.cleaned_data['type']
            if plan_type == Plan.GRAPH_TYPE:
                self.success_url = reverse_lazy('graph:to_plan', args=[plan.slug])
            elif plan_type == Plan.TABLE_TYPE:
                self.success_url = reverse_lazy('table:to_plan', args=[plan.slug])

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

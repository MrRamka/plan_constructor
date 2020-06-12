import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.views import View

from core.forms import CreatePlanForm
from core.models import Plan, UserColor, Color


class HomeView(LoginRequiredMixin, TemplateView):
    """
    Main page with all main information
    """
    template_name = 'core/home.html'
    items_amount = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)

        graph_plans = Plan.graph_plan_objects.filter(author=self.request.user).order_by('last_update')[
                      :self.items_amount]
        table_plans = Plan.table_plan_objects.filter(author=self.request.user).order_by('last_update')[
                      :self.items_amount]

        context_data['graph_plans'] = graph_plans
        context_data['table_plans'] = table_plans

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


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'core/settings.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)

        # add user colors
        user_colors = Color.custom_color.filter(author=self.request.user)
        context_data['user_colors'] = user_colors

        # menu item
        context_data['settings'] = True
        return context_data


class AddColorView(LoginRequiredMixin, View):
    def post(self, request):
        if request.is_ajax():
            color_name = request.POST.get('color_name', None)
            color_description = request.POST.get('color_description', None)
            color_hex = request.POST.get('color_hex', None)
            Color.objects.create(
                author=request.user,
                name=color_name,
                description=color_description,
                hex=color_hex,
                type=Color.CUSTOM_COLOR
            )
            data = {
                'status': 'Ok'
            }
            return HttpResponse(json.dumps(data), content_type='application/json')

from django.forms import ModelForm

from core.models import Plan


class CreatePlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'type', 'description', 'version']
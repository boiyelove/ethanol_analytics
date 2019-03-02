from django import forms
from .models import Experiment

class ExperimentForm(forms.ModelForm):
	class Meta:
		model = Experiment
		exclude = ('created', 'updated', 'created_by', 'modified_by')
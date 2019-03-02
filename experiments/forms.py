from django import forms
from .models import Experiment

class ExperimentForm(forms.ModelForm):
	class Meta:
		model = Experiment
		exclude = ('created', 'updated', 'created_by', 'modified_by')
		widgets = {
		'goal': forms.Textarea(attrs={'rows':3}),
		'start_date': forms.SelectDateWidget(),
		'end_date': forms.SelectDateWidget(),
		}
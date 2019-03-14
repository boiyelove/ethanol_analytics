from django import forms
from .models import Experiment


class ExperimentForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ExperimentForm, self).__init__(*args, **kwargs)
		self.fields['assets'].empty_label=None

	class Meta:
		model = Experiment
		exclude = ('active_flag', 'status', 'created_by', 'modified_by')
		widgets = {
		'goal': forms.Textarea(attrs={'rows':3}),
		'assets': forms.CheckboxSelectMultiple,
		}

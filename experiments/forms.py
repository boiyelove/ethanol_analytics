from django import forms
from .models import Experiment, ASSET_CHOICES


class ExperimentForm(forms.ModelForm):
	assets = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=ASSET_CHOICES)


	class Meta:
		model = Experiment
		exclude = ('active_flag', 'status', 'created_by', 'modified_by')
		widgets = {
		'goal': forms.Textarea(attrs={'rows':3}),
		}

	def clean_assets(self):
		assets = self.cleaned_data.get('assets')
		assets = ','.join(assets)
		return assets
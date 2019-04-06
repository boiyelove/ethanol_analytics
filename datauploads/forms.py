from django import forms
from .models import DataUpload, DataFileUpload


class DataFileUploadForm(forms.ModelForm):
	class Meta:
		model = DataFileUpload
		fields = ('csv_file',)

class DataUploadForm(forms.ModelForm):
	class Meta:
		model = DataUpload
		exclude = ['created', 'updated']
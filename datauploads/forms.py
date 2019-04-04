from django import forms
from .models import DataUpload, DataFileUpload


class DataFileUploadForm(models.ModelForm):
	class Meta:
		model = DataFileUpload
		field = ('csv_file')

class DataUploadForm(models.ModelForm):
	class Meta:
		model = DataUpload
		exclude = ['created', 'updated']
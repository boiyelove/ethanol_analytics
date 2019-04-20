from django import forms
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from core.forms import 	FormLink
from core.views import BasicAccess
from .models import  AnomalyData

# Create your views here.
class AnomalyDetectionView(BasicAccess, TemplateView):
	template_name = "anomaly_detection/anomaly_detection.html"

	def get_context_data(self, **kwargs):
		id = kwargs.get('id', None)
		if id:
			kwargs['anomaly_item'] = AnomalyData.objects.get(id=id)
			kwargs['use_plotlydash'] = True
			self.template_name = "anomaly_detection/anomaly_detection_detail.html"
		return super().get_context_data(**kwargs)

class AnomalyDataCreateView(BasicAccess, CreateView):
	model = AnomalyData
	fields = ['sensor_id', 'anomaly_start', 'anomaly_end', 'asset_category']
	success_url = reverse_lazy('anomaly_detection:anomaly-view')
	template_name = 'core/forms.html'
	extra_context = {'form_name': 'Anomally Data', 'exit_link': FormLink('Back to List', reverse_lazy('anomaly_detection:anomaly-view'))}

	def get_form(self, form_class):
		form = super(AnomalyDataCreateView, self).get_form(form_class)
		form.fields['anomaly_start'].widget = forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
		form.fields['anomaly_end'].widget = forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker2'
        })
		return form
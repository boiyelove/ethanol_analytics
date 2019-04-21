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
	success_url = reverse_lazy('anomaly_detection:view-anomaly')
	template_name = 'anomaly_detection/anomaly_form.html'
	extra_context = {'form_name': 'Anomaly Data', 'exit_link': FormLink('Back to List', reverse_lazy('anomaly_detection:view-anomaly'))}

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['anomaly_start'].input_formats = ['%d/%m/%Y %H:%M']
		form.fields['anomaly_end'].input_formats = ['%d/%m/%Y %H:%M']
		return form

	def form_invalid(self, form):
		print('post is', self.request.POST)
		print('form is', form)
		return super().form_invalid(form)
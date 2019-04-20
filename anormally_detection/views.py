from django.views.generic import TemplateView
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
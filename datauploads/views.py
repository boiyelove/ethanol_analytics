from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import  get_report_data

# Create your views here.
class DataUploadView(LoginRequiredMixin, TemplateView):
	template_name = "datauploads/datalist.html"


	def get_context_data(self, **kwargs):
		id = kwargs.get('id', None)
		if id:
			kwargs['data_item'] = get_report_data(id=id)
			kwargs['use_plotlydash'] = True
			self.template_name = "datauploads/datalist.html"
		else:
			kwargs['data_list'] = get_report_data()
		return super().get_context_data(**kwargs)
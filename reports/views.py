from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import  get_report_data

# Create your views here.
class ReportView(LoginRequiredMixin, TemplateView):
	template_name = "reports/reports.html"
	# extra_context = {"reportlist": get_report_data, "page_title": "Reports"}

	def get_context_data(self, **kwargs):
		id = kwargs.get('id', None)
		if id:
			kwargs['report_item'] = get_report_data(id=id)
			kwargs['use_plotlydash'] = True
			self.template_name = "reports/reports_detail.html"
		return super().get_context_data(**kwargs)
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import  get_report_data

# Create your views here.
class ReportView(LoginRequiredMixin, TemplateView):
	template_name = "reports/reports.html"
	extra_context = {"reportlist": get_report_data, "page_title": "Reports"}

from django.views.generic import TemplateView
from django.forms import formset_factory
from django.forms.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import  get_report_data
from .forms import DataUploadForm, DataFileUploadForm

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

class DataUploadForm(LoginRequiredMixin, FormView):
	template_name = 'core/forms.html'
	form = formset_factory(DataUploadForm)

	def get_context_data(self, **kwargs):
		f_t = kwargs.get('form', 'file')
		if f_t == 'file':
			self.form_class = DataFileUploadForm
		return super().get_context_data(**kwargs)
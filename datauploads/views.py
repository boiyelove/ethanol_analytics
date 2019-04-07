from django.views.generic import TemplateView
from django.forms import formset_factory
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import  get_uploaddata
from .forms import DataUploadForm, DataFileUploadForm

# Create your views here.
class DataUploadView(LoginRequiredMixin, TemplateView):
	template_name = "datauploads/datalist.html"


	def get_context_data(self, **kwargs):
		id = kwargs.get('id', None)
		if id:
			kwargs['data_item'] = get_uploaddata(id=id)
			kwargs['use_plotlydash'] = True
			self.template_name = "datauploads/data_detail.html"
		return super().get_context_data(**kwargs)

class DataUploadForm(LoginRequiredMixin, FormView):
	template_name = 'datauploads/data_uploadform.html'
	form_class = formset_factory(DataUploadForm, extra=4)

	def get_context_data(self, **kwargs):
		f_t = kwargs.get('form', 'form')
		if f_t == 'file':
			self.form_class = DataFileUploadForm
			self.template_name = 'core/forms.html'
			kwargs['form_name'] = "Update Data CSV"
		return super().get_context_data(**kwargs)
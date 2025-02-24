from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.models import User
from core.models import get_latest_data
from core.views import BasicAccess
from .forms import ExperimentForm
from .models import Experiment, get_assets

# Create your views here.
class CreateExperiment(BasicAccess, FormView):
	form_class = ExperimentForm
	success_url = reverse_lazy('experiments:list-experiments')
	template_name = 'experiments/experiment_form.html'

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.created_by = self.request.user.username
		self.object.add_to_db()
		return HttpResponseRedirect(self.success_url)


class UpdateExperiment(BasicAccess, UpdateView):
	form_class = ExperimentForm
	success_url = reverse_lazy('list-experiments')
	template_name = 'experiments/experiment_form.html'

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.modified_by.add(self.request.user)
		self.object.save()
		return HttpResponseRedirect(self.success_url)


class ExperimentList(BasicAccess, ListView):
	model = Experiment
	template_name = 'experiments/experiment_list.html'

class ExperimentDetail(BasicAccess, DetailView):
	model = Experiment
	template_name = 'experiments/experiment_results.html'

	def get_context_data(self, **kwargs):
		kwargs = super().get_context_data(**kwargs)
		sensor_id = self.request.GET.get("sensor_id", None)

		kwargs['use_plotlydash'] = True
		kwargs['sensor_id'] = sensor_id
		return kwargs


class ExperimentResultView(BasicAccess, TemplateView):
	template_name = 'experiments/experiment_results.html'

	def get_context_data(self, **kwargs):
		kwargs = super().get_context_data(**kwargs)
		sensor_id = self.request.GET.get("sensor_id", None)
		kwargs['use_plotlydash'] = True
		kwargs['sensor_id'] = sensor_id
		return kwargs





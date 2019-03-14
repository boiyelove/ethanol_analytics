from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from .forms import ExperimentForm
from .models import Experiment, get_assets

# Create your views here.
class CreateExperiment(CreateView):
	form_class = ExperimentForm
	success_url = reverse_lazy('experiments:list-experiments')
	template_name = 'experiments/experiment_form.html'

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.created_by = self.request.user
		self.object.save()
		return HttpResponseRedirect(self.success_url)

class UpdateExperiment(UpdateView):
	form_class = ExperimentForm
	success_url = reverse_lazy('list-experiments')
	template_name = 'experiments/experiment_form.html'

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.modified_by.add(self.request.user)
		self.object.save()
		return HttpResponseRedirect(self.success_url)


class ExperimentList(ListView):
	model = Experiment
	template_name = 'experiments/experiment_list.html'

class ExperimentDetail(DetailView):
	model = Experiment
	template_name = 'experiments/experiment_detail.html'
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from .forms import ExperimentForm
from .models import Experiment

# Create your views here.
class CreateExperiment(CreateView):
	form = ExperimentForm
	success_url = reverse_lazy('list-experiments')
	template_name = 'experiments/forms.html'

	def form_valid(self, form):
		form.author = self.request.user
		return super().form_valid(form)

class UpdateExperiment(UpdateView):
	form = ExperimentForm
	success_url = reverse_lazy('list-experiments')
	template_name = 'experiments/forms.html'

	def form_valid(self, form):
		form.author = self.request.user
		return super().form_valid(form)

class ExperimentList(ListView):
	model = Experiment
	template_name = 'experiments/experiment_list.html'

class ExperimentDetail(DetailView):
	model = Experiment
	template_name = 'experiments/experiment_detail.html'
from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class LayoutView(TemplateView):
	template_name = 'core/layout.html'
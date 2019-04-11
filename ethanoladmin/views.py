from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.views import CanViewContentTest
# Create your views here.


class AdminMain(oginRequiredMixin, CanViewContentTest, TemplateView):
	template_name = 'ethanoladmin/admin_main.html'

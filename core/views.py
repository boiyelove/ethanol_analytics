from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import UserAccessRequest

# Create your views here.
def custom_403(request):
	render (request, {}, 'core/403.html')

class CanViewContentTest:
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_superuser:
			return super().dispatch(*args, **kwargs)
		else:
			try:
				useraccessrequest = UserAccessRequest.objects.get(user =  request.user)
				if useraccessrequest.is_allowed:
					return super().dispatch(request, *args, **kwargs)
			except:
				return HttpResponseRedirect(reverse_lazy('core:permission-error'))

class LayoutView(LoginRequiredMixin, TemplateView):
	template_name = 'core/layout.html'

class DashboardView(LoginRequiredMixin, CanViewContentTest, TemplateView):
	template_name = 'core/dashboard.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['permission_requests'] = UserAccessRequest.objects.all()
		return context

class PermissionRequiredView(LoginRequiredMixin, TemplateView):
	template_name = 'core/permission_required.html'

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		try:
			useraccessrequest = UserAccessRequest.objects.get(user =  request.user)
			context['access_granted'] = True
		except:
			context['access_granted'] = False
		return self.render_to_response(context)


	def post(self, request, *args, **kwargs):
		UserAccessRequest.objects.create(user = request.user)
		context = self.get_context_data(**kwargs)
		context['access_granted'] = True
		return self.render_to_response(context)


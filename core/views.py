from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, Http404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import UserAccessRequest, get_sensor_data
from .forms import BugReportForm
from easy_pdf.views import PDFTemplateView

class HelloPDFView(PDFTemplateView):
	template_name = "something.html"

# Create your views here.

class CanViewContentTest:
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_superuser:
			return super().dispatch(request, *args, **kwargs)
		else:
			try:
				useraccessrequest = UserAccessRequest.objects.get(user =  request.user)
				if useraccessrequest.is_allowed:
					return super().dispatch(request, *args, **kwargs)
			except:
				return HttpResponseRedirect(reverse_lazy('core:permission-error'))

# class LayoutView(LoginRequiredMixin, TemplateView):
# 	template_name = 'core/login.html'

class DashboardView(LoginRequiredMixin, CanViewContentTest, TemplateView):
	template_name = 'core/dashboard.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['permission_requests'] = UserAccessRequest.objects.all()
		sensor_data = get_sensor_data()
		sensor_list = [{"sensor_id": sensor['sensor_id'], "sensor_description":sensor['sensor_description']} for sensor in sensor_data]
		sensor_id = self.request.GET.get("sensor_id", None)
		entries = self.request.GET.get("entries", 50)
		if sensor_id:
			sensor_data = get_sensor_data(sensor_id= "'" + sensor_id + "'", n=entries)
		else:
			sensor_data = get_sensor_data()
		sensor_list = [dict(tupled) for tupled in set(tuple(sensor.items()) for sensor in sensor_list)]

		context['sensor_id'] = sensor_id
		context['entries'] = entries
		context['sensor_list'] = sensor_list
		context['sensor_data'] = sensor_data
		context['freq'] = 'week'
		return context

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			form_name = request.POST.get('form-name')
			if form_name == 'permission_request_form':
				user = User.objects.get(id=int(request.POST.get('user_id')))
				permission_status = request.POST.get('permission_status')
				useraccessrequest = user.useraccessrequest
				if permission_status == True:
					useraccessrequest.is_allowed = True
					useraccessrequest.save()
				else:
					useraccessrequest.is_allowed = False
					useraccessrequest.save()
			return HttpResponse('something')
		raise Http404

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

class ReportBugFV(LoginRequiredMixin, FormView):
	template_name = 'core/forms.html'
	form_class = BugReportForm
	success_url = reverse_lazy('core:dashboard')

	def form_valid(self, form):
		send_bugreport = form.send_bug_report()
		return super().form_valid(form)
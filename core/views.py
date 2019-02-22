from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, Http404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import UserAccessRequest, get_sensor_data, get_latest_data
from .forms import BugReportForm
from easy_pdf.views import PDFTemplateView


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
		freq = self.request.GET.get("freq", 'week')
		print('frequency is', freq)
		entries = self.request.GET.get("entries", 10)
		if sensor_id:
			sensor_data = get_sensor_data(sensor_id= "'" + sensor_id + "'", n=entries)
		else:
			sensor_data = get_sensor_data()
		sensor_list = [dict(tupled) for tupled in set(tuple(sensor.items()) for sensor in sensor_list)]
		if (sensor_id and sensor_data): context['sensor_latest'] = sensor_data[0]

		# if sensor_id: x for x in latest_dataset if x.get('sensor_id') == sensor_id

		latest_dataset = get_latest_data()
		latest_dataset = sorted(latest_dataset, key=lambda k: k["sensor_description"])
		context['latest_dataset'] = latest_dataset
		context['freq'] = freq
		context['sensor_id'] = sensor_id
		context['entries'] = entries
		context['sensor_list'] = sensor_list
		context['sensor_data'] = latest_dataset
		return context



	# def render_to_pdfresponse(self, **response_kwargs):
	# 	self.template_name = 'core/pdf_template.html'
	# 	self.pdf_filename = 'sensor_data.pdf'
	# 	self.content_type = 'application/pdf'
	# 	pdf_view = .as_view()(self.request)
	# 	return PDFTemplateResponseMixin.get_pdf_response(self.get_context_data(), **response_kwargs)





# def donation_receipt(request, donation_id):
#     donation = get_object_or_404(Donation, pk=donation_id, user=request.user)
#     response = HttpResponse(content_type="application/pdf")
#     response['Content-Disposition'] = "inline; filename={date}-{name}-donation-receipt.pdf".format(
#         date=donation.created.strftime('%Y-%m-%d'),
#         name=slugify(donation.donor_name),
#     )
#     html = render_to_string("donations/receipt_pdf.html", {
#         'donation': donation,
#     })

#     font_config = FontConfiguration()
#     HTML(string=html).write_pdf(response, font_config=font_config)
#     return response

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
		# filetype  = request.POST.get('filetype', None)
		# if filetype == 'pdf':
		# 	return self.render_to_pdfresponse(**kwargs)
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


class DownloadPDF(LoginRequiredMixin, PDFTemplateView):
	template_name = "core/pdf_template.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		sensor_data = get_sensor_data()
		sensor_list = [{"sensor_id": sensor['sensor_id'], "sensor_description":sensor['sensor_description']} for sensor in sensor_data]
		sensor_id = self.request.GET.get("sensor_id", None)
		entries = self.request.GET.get("entries", 50)
		if sensor_id:
			sensor_data = get_sensor_data(sensor_id= "'" + sensor_id + "'", n=entries)
		else:
			sensor_data = get_sensor_data()
		sensor_list = [dict(tupled) for tupled in set(tuple(sensor.items()) for sensor in sensor_list)]
		# self.pdf_filename = 'sensor_data.pdf'
		context['sensor_id'] = sensor_id
		context['entries'] = entries
		context['sensor_list'] = sensor_list
		context['sensor_data'] = sensor_data
		context['freq'] = 'week'
		return super().get_context_data(pagesize="A4 landscape",**context)


# def do_pdf():
# 	from django.contrib.auth.decorators import login_required
# 	from django.template.loader import get_template
# 	from django.template import RequestContext
# 	from django.http import HttpResponse
# 	from django.conf import settings

# 	from weasyprint import HTML, CSS

# 	@login required
# 	def get_report(request):
# 	    html_template = get_template('templates/report.html')
# 	    user = request.user

# 	    rendered_html = html_template.render(RequestContext(request, {'you': user})).encode(encoding="UTF-8")

# 	    pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[CSS(settings.STATIC_ROOT +  'css/report.css')])

# 	    http_response = HttpResponse(pdf_file, content_type='application/pdf')
# 	    http_response['Content-Disposition'] = 'filename="report.pdf"'

# 	    return response
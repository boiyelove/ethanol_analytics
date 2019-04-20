from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from core.models import UserAccessRequest, Sensor
from core.views import BasicAccess
from .models import get_allsensors

# Create your views here.
class AdminMain(BasicAccess, UserPassesTestMixin, TemplateView):
	template_name = 'ethanoladmin/admin_main.html'

	def test_func(self):
		return self.request.user.is_superuser


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['permission_requests'] = UserAccessRequest.objects.	all()
		context['all_sensor_list'] = get_allsensors()
		context['selected_sensors'] = Sensor.objects.filter(show_on_dashboard = True).values_list('sensor_id', flat=True)
		return context



	def post(self, request, *args, **kwargs):

		if request.is_ajax():
			print('post data is', request.POST)

			# form name = permission request
			form_name = request.POST.get('form-name', None)
			if form_name == "permission_request_form":
				print('in pemission block')
				try:
					useraccessrequest =UserAccessRequest.objects.get(id=int(request.POST.get('accessid')))
					permission_status = int(request.POST.get('permission_status'))
					if permission_status == 1:
						useraccessrequest.is_allowed = True
						useraccessrequest.save()
					elif permission_status == 0:
						useraccessrequest.is_allowed = False
						useraccessrequest.save()
					print('in pemission block')
					return JsonResponse({
						'accessid': useraccessrequest.id,
						'access_request': useraccessrequest.is_allowed,
						})
				except Exception as e:
					# throw error
					print(e)

			# form name  = sensor form
			if form_name == "sensorform":
				print('in sensor block')
				try:
					select_status = int(request.POST.get('select_status'))
					sensor_id = request.POST.get('sensor_id')
					obj, created = Sensor.objects.get_or_create(sensor_id = sensor_id)
					if select_status == 1:
						if not created:
							obj.show_on_dashboard =True
							obj.save()
					elif select_status == 0:
						obj.show_on_dashboard = False
						obj.save()
					print('in sensor block')
					return JsonResponse({
						'sensor_id': obj.sensor_id,
						'show_on_dashboard': obj.show_on_dashboard,
						})
				except Exception as e:
					print(e)
					# throw error
			# get selected sensors
			# if exists
			# delect all
			# get or create sensor
			#set to active
			#done

				
		raise Http404


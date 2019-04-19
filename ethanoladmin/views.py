from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from core.models import UserAccessRequest
from core.views import BasicAccess
from .models import get_allsensors

# Create your views here.
class AdminMain(BasicAccess, UserPassesTestMixin, TemplateView):
	template_name = 'ethanoladmin/admin_main.html'

	def test_func(self):
		return self.request.user.is_superuser


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['permission_requests'] = UserAccessRequest.objects.all()
		context['all_sensor_list'] = get_allsensors()
		return context



	def post(self, request, *args, **kwargs):
		if request.is_ajax():

			try:
				useraccessrequest =UserAccessRequest.objects.get(id=int(request.POST.get('accessid')))
				permission_status = int(request.POST.get('permission_status'))
				if permission_status == 1:
					useraccessrequest.is_allowed = True
					useraccessrequest.save()
				elif permission_status == 0:
					useraccessrequest.is_allowed = False
					useraccessrequest.save()
				return JsonResponse({
					'accessid': useraccessrequest.id,
					'access_request': useraccessrequest.is_allowed,
					})
			except e:
				print(e)

			# selected_sensors = request.POST.get('selected_sensors')
			# get selected sensors
			# if exists
			# delect all
			# get or create sensor
			#set to active
			#done

				
		raise Http404


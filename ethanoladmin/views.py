from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import UserAccessRequest
from core.views import CanViewContentTest

# Create your views here.


class AdminMain(LoginRequiredMixin, CanViewContentTest, TemplateView):
	template_name = 'ethanoladmin/admin_main.html'


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['permission_requests'] = UserAccessRequest.objects.all()
		return context



	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			# form_name = request.POST.get('form-name')
			# if form_name == 'permission_request_form':
			try:
				useraccessrequest =UserAccessRequest.objects.get(id=int(request.POST.get('accessid')))
				permission_status = request.POST.get('permission_status')
				print('request.post is', request.POST)
				print('permission_status is', permission_status)
				if permission_status == True:
					useraccessrequest.is_allowed = True
					useraccessrequest.save()
				else:
					useraccessrequest.is_allowed = False
					useraccessrequest.save()
				return JsonResponse({
					'accessid': useraccessrequest.id,
					'access_request': useraccessrequest.is_allowed,
					})
			except e:
				print(e)
				
		raise Http404


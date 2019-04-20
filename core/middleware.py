from django.utils.timezone import now


class LastAccessedMiddleware(object):
	def __init__(self, get_response):
		self.get_response = get_response


	def __call__(self, request):
		if request.user.is_authenticated:
			useraccess = request.user.useraccess
			useraccess.last_access = now()
			useraccess.save()
		response = self.get_response(request)
		return response





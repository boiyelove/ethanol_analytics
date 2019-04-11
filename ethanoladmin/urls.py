from django.urls import path
from . import views

urlpatterns = [
	path('', views.AdminMain.as_view(), name='view-admin'),
	]
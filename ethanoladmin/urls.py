from django.urls import path
from . import views

app_name ='ethanoladmin'
urlpatterns = [
	path('', views.AdminMain.as_view(), name='view-admin'),
	]
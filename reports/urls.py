from django.urls import path
from .dashapps import dash_app1, dash_app2, dash_app3
from . import views


app_name ='reports'

urlpatterns =  [
	path('', views.ReportView.as_view(), name='view-report'),
	path('<int:id>/', views.ReportView.as_view(), name='view-report_detail'),
]

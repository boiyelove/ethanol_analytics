from django.urls import path
from . import views


app_name ='core'

urlpatterns =  [
	path('', views.DashboardView.as_view(), name='dashboard-base'),
	path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
	# path('layout/', views.LayoutView.as_view(), name='layout'),
	path('permission_required/', views.PermissionRequiredView.as_view(), name='permission-error'),
	path('report_bug/', views.ReportBugFV.as_view(), name='report-bug'),
	path('download_pdf/', views.DownloadPDF.as_view(), name='download-pdf'),

]
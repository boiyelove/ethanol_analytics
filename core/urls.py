from django.urls import path
from django.utils.functional import curry
from . import views


app_name ='core'

urlpatterns =  [
	path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
	path('layout/', views.LayoutView.as_view(), name='layout'),
	path('permission_required/', views.PermissionRequiredView.as_view(), name='permission-error'),
]

handler403 = 'ethanol_analytic.core.views.custom_403'
from django.urls import path
from .dashapps import dash_app1, dash_app2, dash_app3
from . import views


app_name ='datauploads'

urlpatterns =  [
	path('', views.DataUploadView.as_view(), name='view-dataupload'),
	path('<int:id>/', views.DataUploadView.as_view(), name='view-dataupload_detail'),
]

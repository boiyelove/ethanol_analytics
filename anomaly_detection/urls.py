from django.urls import path
from .dashapps import dash_app1, dash_app2, dash_app3
from . import views


app_name ='anomaly_detection'

urlpatterns =  [
	path('', views.AnomalyView.as_view(), name='view-anomaly'),
	path('<int:id>/', views.AnomalyView.as_view(), name='view-anomaly_detail'),
]

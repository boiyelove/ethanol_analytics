from django.urls import path
from .dashapps import dash_app3
from . import views


app_name ='anomaly_detection'

urlpatterns =  [
	path('', views.AnomalyDetectionView.as_view(), name='view-anomaly'),
	path('<int:id>/', views.AnomalyDetectionView.as_view(), name='view-anomaly_detail'),
	# path('add/', views.AnomalyDataCreateView.as_view(), name='add-anomalydata'),
]

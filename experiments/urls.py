from django.urls import path
from . import views

app_name="experiments"

urlpatterns = [
	path('', views.ExperimentList.as_view(), name='list-experiments' ),
	path('create/', views.CreateExperiment.as_view(), name='create-experiment'),
	path('<int:pk>/', views.ExperimentDetail.as_view(), name='view-experiment'),
	path('<int:id>/edit/', views.UpdateExperiment.as_view(), name='edit-experiment'),
	]
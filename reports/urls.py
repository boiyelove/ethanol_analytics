from django.urls import path
from .dashapps import dash_app1
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name ='reports'

urlpatterns =  [
	path('', views.ReportView.as_view(), name='view-report'),
	path('<int:id>/', views.ReportView.as_view(), name='view-report_detail'),
]

# Add in static routes so daphne can serve files; these should
# be masked eg with nginx for production use

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

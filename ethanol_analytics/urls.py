"""ethanol_analytics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('allauth.urls')),
    path('', include('core.urls')),
    path('reports/', include('reports.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('experiments/', include('experiments.urls')),
    path('data_uploads/', include('datauploads.urls')),
    path('ethanoladmin/', include('ethanoladmin.urls')),
    path('anomaly_detection/', include('anomaly_detection.urls')),
]

# Add in static routes so daphne can serve files; these should
# be masked eg with nginx for production use
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.contrib import admin
from .models import Asset, Experiment, Metric, AssetCategory
# Register your models here.

app_models = [Asset, Metric, AssetCategory]
for model in app_models:admin.site.register(model)
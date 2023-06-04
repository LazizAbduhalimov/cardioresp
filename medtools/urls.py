from django.urls import path
from .views import *

urlpatterns = [
    path('tools/', ToolsPage.as_view(), name="tools"),
    path('tools/heart/', HeartDiseaseToolPage.as_view(), name="heart-disease-tool"),
    path('tools/heart/update/<int:pk>/', HeartDiseaseToolUpdatePage.as_view(), name="heart-disease-tool-update"),
]
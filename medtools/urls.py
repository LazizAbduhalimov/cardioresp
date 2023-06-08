from django.urls import path
from .views import *

urlpatterns = [
    path('tools/heart/', HeartDiseaseToolPage.as_view(), name="heart-disease-tool"),
    path('tools/heart/update/<int:pk>/', HeartDiseaseToolUpdatePage.as_view(), name="heart-disease-tool-update"),
    path('tools/heart/survey/<int:pk>/', SurveyPage.as_view(), name="heart-disease-survey"),
    path('tools/heart/survey/multiple/<int:pk>/', SurveyMultipleChoicePage.as_view(), name="heart-disease-survey-multiple-choice"),
]
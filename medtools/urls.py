from django.urls import path
from .views import *

urlpatterns = [
    path('tools/heart/', HeartDiseaseToolPage.as_view(), name="heart-disease-tool"),
    path('tools/heart/update/<int:pk>/', HeartDiseaseToolUpdatePage.as_view(), name="heart-disease-tool-update"),
    path('tools/heart/delete/<int:pk>/', HeartDiseaseToolDeletePage.as_view(), name="heart-disease-tool-delete"),
    path('tools/heart/survey/', SurveyPage.as_view(), name="heart-disease-survey"),
    path('tools/heart/survey-multiple/', SurveyMultipleChoicePage.as_view(), name="heart-disease-survey-multiple-choice"),
    path('docx/<int:pk>/', GetDocxFile, name='docx-file-download')
]
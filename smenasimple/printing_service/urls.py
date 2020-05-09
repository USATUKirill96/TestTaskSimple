from django.conf.urls import url
from . import views

app_name = "printing_service"

urlpatterns = [
    url(r'^create_checks/', views.CreateChecks.as_view()),
    url(r'^new_checks/', views.NewChecks.as_view()),
    url(r'check/', views.CheckToPrint.as_view()),
]
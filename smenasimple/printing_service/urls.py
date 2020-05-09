from django.conf.urls import url
from . import views

app_name = "printing_service"

urlpatterns = [
    url(r'^create_checks/', views.CreateChecks.as_view()),
    url(r'^new_checks/', views.new_checks),
    url(r'check/', views.check),
]
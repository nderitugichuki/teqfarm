from django.urls import path
from .views import ReportView

urlpatterns = [path("<slug:report_type>/", ReportView.as_view(), name="report")]


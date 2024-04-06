from django.urls import path
from .views import SpreadsheetUploadView

urlpatterns = [
    path('v1/spreadsheet/<str:table_name>/', SpreadsheetUploadView.as_view(), name='upload_spreadsheet'),
]
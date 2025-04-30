from django.urls import path
from .views import report_form_view

urlpatterns = [
    path('', report_form_view, name='report_form'),
]
from django.urls import path
from django.views.generic import TemplateView

from .views import JobsListView

urlpatterns = [
    path('', JobsListView.as_view(), name='home'),
    path('jobs/confirm/', TemplateView.as_view(template_name='jobs_confirmation.html'), name='jobs_confirmation')
]

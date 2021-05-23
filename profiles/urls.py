from django.urls import path

from .views import ProfileView

urlpatterns = [
    path('accounts/profile/', ProfileView.as_view(), name='account_profile'),
]
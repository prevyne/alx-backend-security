from django.urls import path
from . import views

urlpatterns = [
    # This creates a path for the test view
    path('test/', views.test_api_view, name='test_api'),
]
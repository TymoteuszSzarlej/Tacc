from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='tasktrack_dashboard'),  # Strona główna (landing page)
]
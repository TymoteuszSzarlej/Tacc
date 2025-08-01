from django.urls import path
from .views import *

urlpatterns = [
    path('', landing_page, name='landing_page'),  # Strona główna (landing page)
    path('apps/', apps, name='apps'),  # Widok dla aplikacji
]
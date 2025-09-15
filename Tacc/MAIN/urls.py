from django.urls import path
from .views import *

urlpatterns = [
    path('', landing_page, name='landing_page'),  # Strona główna (landing page)
    path('versions/', get_list_of_versions, name='versions'),  # Strona z wersjami
    path("remove-session-message/", remove_session_message, name="remove_session_message"),

]
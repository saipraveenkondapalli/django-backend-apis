from django.urls import path
from .views import main_resume, contact_send_email

urlpatterns = [
    path('resume/', main_resume, name='resume'),
    path('email/', contact_send_email, name='contact_send_email'),
]

from django.urls import path
from .views import main_resume, contact_send_email, BlogDetailView

urlpatterns = [
    path('resume/', main_resume, name='resume'),
    path('email/', contact_send_email, name='contact_send_email'),
    path('blog/<str:slug>/', BlogDetailView.as_view(), name='get_blog'),
]

from django.urls import path
from .views import copy_page, web, job_application, main_resume

urlpatterns = [
    path('copy_page/<uuid:pk>/', copy_page, name='copy_page'),
    path('web/', web, name='web'),

    path('job/track/', job_application, name='test_job_application')
]

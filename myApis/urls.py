"""
URL configuration for myApis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "MyApis Admin"
admin.site.site_title = "MyApis Admin Portal"

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('password_reset/',
                       auth_views.PasswordResetView.as_view(),
                       name='password_reset'),
                  path('password_reset/done/',
                       auth_views.PasswordResetDoneView.as_view(),
                       name='password_reset_done'),
                  path('reset/<uidb64>/<token>/',
                       auth_views.PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
                  path('reset/done/',
                       auth_views.PasswordResetCompleteView.as_view(),
                       name='password_reset_complete'),

                  path('main_site/', include('main_site.urls')),
                  path('api/', include('main_site.apis')),
                  path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

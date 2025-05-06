"""
URL configuration for django_py project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path("index", views.index),
    path("index1", views.index1),
    path("temp_tags", views.temp_tags),
    path("temp_filter", views.temp_filter),
    path("temp_inhreit", views.temp_inhreit),
    path("html_escape", views.html_escape),
    path("login", views.login),
    path("login_check", views.login_check),
    path("check_pwd", views.check_pwd),
    path("check_pwd_action", views.check_pwd_action),
    path("generate_captcha", views.generate_captcha),
    path("url_reverse", views.url_reverse),
    path("static_test", views.static_test),
    path("show_upload", views.show_upload),
    path("upload_handle", views.upload_handle),
    re_path(r"^show_area/(\d*)$", views.show_area),
    re_path(r"^find_areas/(\d*)$", views.find_areas),
    path("areas", views.areas),
    path("test11", views.test),
]

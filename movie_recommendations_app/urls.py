"""recommendations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path
from . import views
# from django.conf.urls import url

app_name = "movie_recommendations_app"


urlpatterns = [
    re_path(r'^$',views.base, name="base"),
    re_path(r'^home/(?P<user>[\w-]+)/(?P<id>[\w-]+)',views.home, name="home"),
    re_path(r'^rec/(?P<user>[\w-]+)/(?P<rec>[\w-]+)',views.graphs,name="graphs")
]

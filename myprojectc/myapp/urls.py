"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$', views.index,name = 'myapp_index'),
    url(r'^index/$', views.index,name = 'myapp_index'),
    url(r'^login/$', views.login,name = 'myapp_login'),
    url(r'^logout/$', views.logout,name = 'myapp_logout'),
    url(r'^register/$', views.register,name = 'myapp_register'),
    url(r'^list/(?P<gid>[0-9]*)$', views.list,name = 'myapp_list'),
    url(r'^info/(?P<gid>[0-9]*)$', views.info,name = 'myapp_info'),
    url(r'^vcode/$', views.vcode,name = 'myapp_vcode'),
    url(r'^testname/$', views.testname,name = 'myapp_testname'),
    url(r'^search/$', views.search,name = 'myapp_search'),

    url(r'^cartlist/$', views.cartlist,name = 'myapp_cartlist'),
   
]


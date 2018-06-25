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
from django.conf.urls import url
from . views import usersviews,typesviews,goodsviews

urlpatterns = [
    # 用户子路由
    url(r'^$', usersviews.index,name = 'myadmin_users_index'),
    url(r'^add/$', usersviews.add,name = 'myadmin_users_add'),
    url(r'^list/$', usersviews.list,name = 'myadmin_users_list'),
    url(r'^delete/$', usersviews.delete,name = 'myadmin_users_delete'),
    url(r'^update/$', usersviews.update,name = 'myadmin_users_update'),
    # 分类子路由
    url(r'^$', usersviews.index,name = 'myadmin_users_index'),
    url(r'^types/add/$', typesviews.add,name = 'myadmin_types_add'),
    url(r'^types/addtop/$', typesviews.addtop,name = 'myadmin_types_addtop'),
    url(r'^types/list/$', typesviews.list,name = 'myadmin_types_list'),
    url(r'^types/delete/$', typesviews.delete,name = 'myadmin_types_delete'),
    url(r'^types/update/$', typesviews.update,name = 'myadmin_types_update'),
    # 商品子路由
    url(r'^$', usersviews.index,name = 'myadmin_users_index'),
    url(r'^goods/add/$', goodsviews.add,name = 'myadmin_goods_add'),
    url(r'^goods/list/$', goodsviews.list,name = 'myadmin_goods_list'),
    url(r'^goods/delete/$', goodsviews.delete,name = 'myadmin_goods_delete'),
    url(r'^goods/update/$', goodsviews.update,name = 'myadmin_goods_update'),
]

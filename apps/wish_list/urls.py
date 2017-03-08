from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.index, name='index'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^wish_items/create$', views.create, name='create'),
    url(r'^add_item$', views.add_item, name='add_item'),
    url(r'^wish_items/(?P<id>\d+)$', views.display_item, name='display_item'),
    url(r'^add_to_list/(?P<id>\d+)$', views.add_to_list, name='add_to_list'),
    url(r'^remove/(?P<id>\d+)$', views.remove, name='remove'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete')
]

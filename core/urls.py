from django.conf.urls import url
from core import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^save/snap/link$', views.save_snap_link, name='save_snap_link'),
    url(r'^my/snap/links$', views.my_snap_links, name='my_snap_links'),
    url(r'^snap/link/details/(?P<id>\d+)$', views.snap_link_details, name='snap_link_details'),
    url(r'^notify/me/price/(?P<link_id>\d+)/(?P<id>\d+)$', views.notify_me_type, name='notify_me_type'),
    url(r'^check/snap/links/new/prices$', views.check_price_change, name='check_price_change'),

]
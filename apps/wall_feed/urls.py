from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^wall$', views.wall_feed),
    url(r'^user_create$', views.user_create),
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),
    url(r'^post_message$', views.post_message),
    url(r'^post_comment/(?P<message_id>\d+)$', views.post_comment),
]
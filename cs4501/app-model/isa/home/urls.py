from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/v1/review/(?P<review_id>[0-9]+)/$', views.review, name='review'),
    url(r'^api/v1/review/create/$', views.review_create, name='review_create'),
    url(r'^api/v1/task/info/(?P<task_id>[0-9]+)/$', views.task_info, name='task_info'),
    url(r'^api/v1/task/create/$', views.task_create, name='task_create'),
    url(r'^api/v1/task/query', views.task, name='task'),
    url(r'^api/v1/user/(?P<user_id>[0-9]+)/$', views.user, name='user'),
    url(r'^api/v1/user/create/$', views.user_create, name='user_create'),
    url(r'^topUsers/$', views.get_top_users, name='get_top_five_users'),
    url(r'^recentListings/$', views.get_recent_listings, name='get_recent_listings'),




]

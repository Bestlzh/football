from django.conf.urls import url
from blog import views

urlpatterns = [

    url(r'^index/',views.index,name='index'),
    url(r'^content/(\d+)$',views.content,name='content'),
    url(r'^content/(\d+)/(\d+)$',views.content,name='content'),
    url(r'^publish/$',views.publish,name='publish'),
    url(r'^search/$',views.search,name='search'),
    url(r'^publish/(\d+)/$',views.publish,name='publish'),
    url(r'^sort_article/$',views.sort_article,name='sort_article'),

]
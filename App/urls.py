from django.conf.urls import url

from App import views

urlpatterns = [

    url(r'^register/',views.register,name='register'),


]
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index), #GET
    url(r'^main$', views.main), #GET
    url(r'^register$', views.register), #POST
    url(r'^login$', views.login), #POST
    url(r'^logout$', views.logout), #POST
    url(r'^success$', views.success), #GET
    url(r'^travels$', views.travels), #GET
    url(r'^travels/add$', views.add), #GET
    url(r'^travels/addPlan$', views.addPlan), #GET
    url(r'^travels/destination/(?P<id>\d+)$', views.destination), #GET
    url(r'^travels/destination/(?P<id>\d+)/join$', views.joinDestination), #GET
]

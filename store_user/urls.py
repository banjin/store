from django.conf.urls import url
from views import my_view, logout_view

urlpatterns = [
    url(r'^login/',  my_view),
    url(r'^logout/', logout_view),
]

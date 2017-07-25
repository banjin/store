from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'question/$', views.create_question)
]

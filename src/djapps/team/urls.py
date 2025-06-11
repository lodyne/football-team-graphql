from django.urls import path
from .views import graphql_view
from django.views.decorators.csrf import csrf_exempt

from djapps.team import views


urlpatterns = [
    path("", views.home, name="home"),
    path("graphql/", csrf_exempt(graphql_view), name = "qraphql")
]

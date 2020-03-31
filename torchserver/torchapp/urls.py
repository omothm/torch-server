from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_request_handler),
    path('contribute/',views.api_contribute_request_handler)
]
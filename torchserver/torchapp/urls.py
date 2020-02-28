from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_get_request),
    #path('banknote/<int:pk>/', views.set_banknote),
]
from django.urls import path
from . import views

urlpatterns = [
    path('banknote/', views.get_banknote),
    path('banknote/<int:pk>/', views.set_banknote),
]
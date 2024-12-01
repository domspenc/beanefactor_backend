from django.urls import path
from . import views

urlpatterns = [
  path('users/', views.DogUserList.as_view()),
  path('users/<int:pk>/', views.DogUserDetail.as_view()),
]
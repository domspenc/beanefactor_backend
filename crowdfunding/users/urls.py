from django.urls import path
from . import views

urlpatterns = [
  path('dogusers/', views.DogUserList.as_view()),
  path('dogusers/<int:pk>/', views.DogUserDetail.as_view()),
  path('dogusers/signup/', views.DogUserSignup.as_view(), name='doguser-signup'),
]
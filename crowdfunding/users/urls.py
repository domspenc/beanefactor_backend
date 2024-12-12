from django.urls import path
from . import views
from .views import DogUserSignup


urlpatterns = [
    path('dogusers/', views.DogUserList.as_view()),
    path('dogusers/<int:pk>/', views.DogUserDetail.as_view()),
    path('dogusers/<int:pk>/projects/', views.DogUserProjects.as_view(), name='user-projects'),  # Add this line
    path('signup/', DogUserSignup.as_view(), name='doguser-signup'),
]
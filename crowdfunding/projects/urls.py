from django.urls import path
from . import views

urlpatterns = [
  path('projects/', views.ProjectList.as_view()),
  path('projects/<int:pk>/', views.ProjectDetail.as_view()),
  path('treatpledges/', views.TreatPledgeList.as_view()),
  path('treatpledges/<int:pk>/', views.TreatPledgeDetail.as_view()),
  path('comments/', views.CommentList.as_view()),  # List and create comments
  path('comments/<int:pk>/', views.CommentDetail.as_view()),  # Retrieve, update, delete a single comment
  path('comments/pledge/<int:pledge_id>/', views.CommentList.as_view()),  # List comments for a specific pledge
  path('categories/', views.CategoryList.as_view()),  # List and create categories
  path('categories/<int:pk>/', views.CategoryDetail.as_view()),  # Retrieve, update, delete a category
]
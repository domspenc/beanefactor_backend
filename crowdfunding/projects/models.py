from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


# CATEGORY MODEL
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # The name of the category
    description = models.TextField(blank=True, null=True)  # Optional description of the category

    def __str__(self):
        return self.name


# --- PROJECT MODEL ---
class Project(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField()
  treat_target = models.IntegerField()
  treat_count = models.IntegerField(
    default=0, 
    validators=[MinValueValidator(0)]) # ensures the count never goes below 0
  image = models.URLField(
      max_length=1000,
      default="https://github.com/domspenc/crowdfunding_backend/raw/main/resources/beanefactor_test_logo.jpg",
      blank=True, null=True
      )
  is_open = models.BooleanField(default=True)
  date_created = models.DateTimeField(auto_now_add=True)
  owner = models.ForeignKey(
    get_user_model(), 
    on_delete=models.CASCADE, 
    related_name='owned_projects')
  categories = models.ManyToManyField(
      'Category', 
      related_name='projects', 
      blank=True)  # Link to categories

  def __str__(self):
      return self.title

# --- TREAT PLEDGE MODEL ---
class TreatPledge(models.Model):
  treats_pledged = models.IntegerField()
  comment = models.CharField(max_length=200)
  anonymous = models.BooleanField()
  project = models.ForeignKey(
    'Project',
    on_delete=models.CASCADE,
    related_name='treat_pledges'
  )
  supporter = models.ForeignKey(
    get_user_model(), 
    on_delete=models.CASCADE, 
    related_name='treat_pledges')
  
class Comment(models.Model):
    content = models.TextField()  # The content of the comment
    date_created = models.DateTimeField(auto_now_add=True)  # Timestamp for the comment
    pledge = models.ForeignKey(
        'TreatPledge', 
        on_delete=models.CASCADE, 
        related_name='comments'  # Link to the pledge
        )
    author = models.ForeignKey(
       get_user_model(), 
       on_delete=models.CASCADE, 
       related_name='comments'
       )

    def __str__(self):
        return f"Comment by {self.author} on pledge {self.pledge.id}"

# class Location(models.Model):
#     city = models.CharField(max_length=100)
#     region = models.CharField(max_length=100, blank=True, null=True)  # Optional field
#     projects = models.ManyToManyField(
#         'Project',
#         related_name='locations'  # Link to projects in this location
#     )

#     def __str__(self):
#         return f"{self.city}, {self.region}" if self.region else self.city

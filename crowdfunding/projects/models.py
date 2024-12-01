from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
# --- PROJECT MODEL ---
class Project(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField()
  treat_target = models.IntegerField()
  # treat_count = models.IntegerField(
  #   default=0, 
  #   validators=[MinValueValidator(0)]) # ensures the count never goes below 0
  image = models.URLField()
  is_open = models.BooleanField()
  date_created = models.DateTimeField(auto_now_add=True)
  owner = models.ForeignKey(
    get_user_model(), 
    on_delete=models.CASCADE, 
    related_name='owned_projects')
  # category = models.ForeignKey(
  #   'Category', 
  #   on_delete=models.SET_NULL, 
  #   null=True, 
  #   related_name="projects")  # Use ForeignKey for categories

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
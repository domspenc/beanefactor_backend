from django.db import models
from django.contrib.auth import get_user_model

# CATEGORY MODEL
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # The name of the category
    description = models.TextField(blank=True, null=True)  # Optional description of the category

    def __str__(self):
        return self.name

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
  # treat_count = models.IntegerField(
  #   default=0, 
  #   validators=[MinValueValidator(0)]) # ensures the count never goes below 0
  image = models.URLField(
      max_length=1000,
      default="https://scontent.fper7-1.fna.fbcdn.net/v/t39.30808-6/369978875_621935253411512_4526444535835746883_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=IcmxA-5_jwUQ7kNvgEpOrIG&_nc_zt=23&_nc_ht=scontent.fper7-1.fna&_nc_gid=AynHdYIiRX3Bq5mt4BSJTaD&oh=00_AYCXXrkgBRoJJiO6HM2TdIz3l7xwPQ4vPtwYNb3fl0CuKw&oe=6759D33C",
      blank=True, null=True
      )
  is_open = models.BooleanField()
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

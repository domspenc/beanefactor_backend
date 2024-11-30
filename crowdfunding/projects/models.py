from django.db import models

# Create your models here.
class Project(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField()
  treat_target = models.IntegerField()
#   treat_count = models.IntegerField(default=0, validators=[MinValueValidator(0)]) # ensures the count never goes below 0
  image = models.URLField()
  is_open = models.BooleanField()
  date_created = models.DateTimeField(auto_now_add=True)
#   owner = models.ForeignKey(DogUser, on_delete=models.CASCADE, related_name="owned_projects")
#   category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="projects")  # Use ForeignKey for categories


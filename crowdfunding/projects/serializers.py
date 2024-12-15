from rest_framework import serializers
from django.apps import apps
from .models import Comment, Category

class TreatPledgeSerializer(serializers.ModelSerializer):
  supporter = serializers.ReadOnlyField(source='supporter.id')
  class Meta:
      model = apps.get_model('projects.TreatPledge')
      fields = '__all__' # aka ['id', 'treats_pledged', 'comment', 'anonymous', 'project', 'supporter']

# class ProjectSerializer(serializers.ModelSerializer):
#   owner = serializers.ReadOnlyField(source='owner.id')
#   image = serializers.ImageField(required=False)  # Ensure it returns the full URL
#   class Meta:
#       model = apps.get_model('projects.Project')
#       fields = '__all__' # aka ['id', 'title', 'description', 'treat_target', 'image', 'is_open', 'date_created', 'owner']

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    image = serializers.ImageField(required=False)

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    class Meta:
        model = apps.get_model('projects.Project')
        fields = '__all__'  # Include the full list of fields, including the image

      

class ProjectDetailSerializer(ProjectSerializer):
  # Meta fields are inherited from ProjectSerializer, so are the same as above with the exception of including treat_pledges
  treat_pledges = TreatPledgeSerializer(many=True, read_only=True)
  
  def update(self, instance, validated_data):
    instance.title = validated_data.get('title', instance.title)
    instance.description = validated_data.get('description', instance.description)
    instance.treat_target = validated_data.get('treat_target', instance.treat_target)
    instance.image = validated_data.get('image', instance.image)
    instance.is_open = validated_data.get('is_open', instance.is_open)
    instance.date_created = validated_data.get('date_created', instance.date_created)
    instance.owner = validated_data.get('owner', instance.owner)
    instance.save()
    return instance

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')  # Automatically set the comment author
    pledge = serializers.ReadOnlyField(source='pledge.id')  # Automatically set the associated pledge

    class Meta:
        model = Comment
        fields = '__all__' # aka ['id', 'content', 'date_created', 'author', 'pledge']

class CategorySerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # List projects associated with this category

    class Meta:
        model = Category
        fields = '__all__' # aka ['id', 'name', 'description', 'projects']

# class LocationSerializer(serializers.ModelSerializer):
#     projects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # List associated projects by their IDs

#     class Meta:
#         model = Location
#         fields = ['__all__'] # aka ['id', 'city', 'region', 'projects']




# {
# 	"title": "Therapy Dogs for Kids",
# 	"description": "This project aims to raise funds to train therapy dogs that will visit children in hospitals, providing comfort, companionship, and emotional support. With every treat pledged, we can help equip a dog with the skills needed to brighten a child's day and provide them with the healing power of a furry friend.",
# 	"treat_target": 1000,
# 	"image": "http://127.0.0.1:8000/media/therapy.jpg",
# 	"is_open": true,
# 	"categories": [1, 10]
# }
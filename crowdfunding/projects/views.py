from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .permissions import IsOwnerOrReadOnly, IsSupporterOrReadOnly, IsAuthorOrReadOnly
from django.http import Http404
from .models import Project, TreatPledge, Comment
from .serializers import ProjectSerializer, TreatPledgeSerializer, ProjectDetailSerializer, CommentSerializer, CategorySerializer

# PROJECTS
class ProjectList(APIView):
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]

  def get(self, request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)
  
  def post(self, request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
  
  def post(self, request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        project = serializer.save(owner=request.user)  # Save the project
        # Link categories to the project
        categories = request.data.get('categories', [])
        project.categories.set(categories)  # Set the categories by their IDs
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # original post request code
    # def post(self, request):
    #     serializer = ProjectSerializer(data=request.data)
    #     if serializer.is_valid():
    #         project = serializer.save(owner=request.user)  # Save the project

    #         # Link categories to the project
    #         categories = request.data.get('categories', [])
    #         project.categories.set(categories)  # Set the categories by their IDs
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class ProjectDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
  
    def get_object(self, pk):
        try:
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)
    
    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(
            instance=project,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):
        project = self.get_object(pk)
        if project.treat_pledges.exists():
            return Response(
            {"error": "Cannot delete a project with active pledges."},
            status=status.HTTP_400_BAD_REQUEST
        )
        project.delete()
        return Response(
            {"message": "Project deleted successfully."},
            status=status.HTTP_200_OK)

# TREAT PLEDGES
class TreatPledgeList(APIView):
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]

  def get(self, request):
      pledges = TreatPledge.objects.all()
      serializer = TreatPledgeSerializer(pledges, many=True)
      return Response(serializer.data)

  def post(self, request):
      serializer = TreatPledgeSerializer(data=request.data)
      if serializer.is_valid():
          serializer.save(supporter=request.user)
          return Response(
              serializer.data,
              status=status.HTTP_201_CREATED
          )
      return Response(
          serializer.errors,
          status=status.HTTP_400_BAD_REQUEST
      )

class TreatPledgeDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsSupporterOrReadOnly]
  
    def get_object(self, pk):
        try:
            pledge = TreatPledge.objects.get(pk=pk)
            self.check_object_permissions(self.request, pledge)
            return pledge
        except TreatPledge.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        pledge = self.get_object(pk)
        serializer = TreatPledgeSerializer(pledge)
        return Response(serializer.data)
    
    def put(self, request, pk):
        pledge = self.get_object(pk)
        serializer = TreatPledgeSerializer(
            instance=pledge,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        pledge = self.get_object(pk)
        pledge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# COMMENTS
class CommentList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request):
        pledge_id = request.data.get('pledge')  # Get the pledge ID from the request data
        if pledge_id:
            try:
                pledge = TreatPledge.objects.get(id=pledge_id, supporter=request.user)  # Ensure the pledge belongs to the user
            except TreatPledge.DoesNotExist:
                return Response({"error": "You must have made a pledge to this project to comment."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Pledge ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Now, save the comment with the pledge
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, pledge=pledge)  # Associate comment with pledge and user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]  # Custom permission for authors

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk):
        return Response({"error": "Comments cannot be modified after creation."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        return Response({"error": "Comments cannot be deleted."}, status=status.HTTP_403_FORBIDDEN)

# CATEGORIES
class CategoryList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(instance=category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
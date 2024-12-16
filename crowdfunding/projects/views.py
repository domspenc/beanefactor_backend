from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .permissions import IsOwnerOrReadOnly, IsSupporterOrReadOnly, IsAuthorOrReadOnly
from django.http import Http404
from .models import Project, TreatPledge, Comment, Category
from .serializers import ProjectSerializer, TreatPledgeSerializer, ProjectDetailSerializer, CommentSerializer, CategorySerializer

# PROJECTS
class ProjectList(APIView):
  permission_classes = [permissions.AllowAny]  # Make it accessible to everyone

  def get(self, request):
    projects = Project.objects.order_by('-date_created')[:8]  # Latest 8 projects
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

  
  def post(self, request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        project = serializer.save(owner=request.user)  # Link project to the logged-in user
        # Link categories to the project
        categories = request.data.get('categories', [])
        project.categories.set(categories)  # Set the categories by their IDs
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectCreate(APIView):
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)  # Assuming the logged-in user is the owner
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
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
        
        # Ensure that the user is the owner of the project
        if project.owner != request.user:
            return Response(
                {"error": "You do not have permission to delete this project."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if the project has active pledges
        if project.treat_pledges.exists():  # Check if there are any active pledges
            return Response(
                {"error": "Cannot delete a project with active pledges."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Delete the project
        project.delete()
        return Response(
            {"message": "Project deleted successfully."},
            status=status.HTTP_200_OK
        )

# TREAT PLEDGES

# This function checks if the project's treat count has reached its target
def update_project_status(project):
    if project.treat_count >= project.treat_target:
        project.is_open = False  # Set the project to closed
        project.save()

class TreatPledgeList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    print(permission_classes)

    def get(self, request):
        pledges = TreatPledge.objects.all()
        serializer = TreatPledgeSerializer(pledges, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        print("Auth Token being used:", request.headers.get('Authorization'))  # Logs the token from the headers
        print("Request user:", request.user)  # Logs the associated user  # Debugging input data
        serializer = TreatPledgeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                pledge = serializer.save(supporter=request.user)
            
                # Increment the treat count for the project
                project = pledge.project
                project.treat_count += pledge.treats_pledged
                project.save()

                # Update the project status after the pledge
                update_project_status(project)

                print("Pledge created successfully:", pledge)  # Debugging successful pledge
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                print("Error saving pledge or updating project:", e)  # Log error details
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            print("Serializer validation failed:", serializer.errors)  # Debugging validation errors
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

# CATEGORIES VIEW
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
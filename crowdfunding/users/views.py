from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import DogUser
from .serializers import DogUserSerializer

# Create your views here.
class DogUserList(APIView):
  def get(self, request):
      users = DogUser.objects.all()
      serializer = DogUserSerializer(users, many=True)
      return Response(serializer.data)

  def post(self, request):
      serializer = DogUserSerializer(data=request.data)
      if serializer.is_valid():
          serializer.save()
          return Response(
              serializer.data,
              status=status.HTTP_201_CREATED
          )
      return Response(
          serializer.errors, 
          status=status.HTTP_400_BAD_REQUEST
      )

class DogUserDetail(APIView):
  def get_object(self, pk):
      try:
          return DogUser.objects.get(pk=pk)
      except DogUser.DoesNotExist:
          raise Http404

  def get(self, request, pk):
      user = self.get_object(pk)
      serializer = DogUserSerializer(user)
      return Response(serializer.data)
  
class CustomAuthToken(ObtainAuthToken):
  def post(self, request, *args, **kwargs):
      serializer = self.serializer_class(
          data=request.data,
          context={'request': request}
      )
      serializer.is_valid(raise_exception=True)
      user = serializer.validated_data['user']
      token, created = Token.objects.get_or_create(user=user)

      return Response({
          'token': token.key,
          'user_id': user.id,
          'email': user.email
      })
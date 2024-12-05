from rest_framework import permissions

# Custom permission to only allow owners to edit or delete their own projects. 
class IsOwnerOrReadOnly(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
      # SAFE_METHODS (GET, HEAD, OPTIONS) are always allowed
      if request.method in permissions.SAFE_METHODS:
          return True
      # Write permissions are only allowed to the owner of the project
      return obj.owner == request.user

# Custom permission to only allow supporters to edit or delete their own pledges.  
class IsSupporterOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS (GET, HEAD, OPTIONS) are always allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the supporter of the pledge
        return obj.supporter == request.user

# Custom permission to only allow the author of a comment to edit or delete it.
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read-only methods for everyone
        return obj.author == request.user  # Allow write methods only for the author
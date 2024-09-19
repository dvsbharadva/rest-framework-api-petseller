from rest_framework import permissions

class IsValidUserPermision(permissions.BasePermission):
    def has_permission(self, request, view):
        # print(request.user)
        # if request.user == "STAFF":
        #     return True
        # return False
        return True
        # return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        return obj.animal_owner == request.user
        # return super().has_object_permission(request, view, obj)
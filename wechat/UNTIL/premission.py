from rest_framework.permissions import BasePermission


######################权限###############3
class MyPermission1(BasePermission):
    message = '必须是svip才能访问'
    def has_permission(self, request, view):
        if request.user.user_type != 3:
            return False #fasle无权访问 true 有权访问
        return True



class MyPermission2(object):
    def has_permission(self, request, view):
        if request.user.user_type != 2:
            return False #fasle无权访问 true 有权访问
        return True
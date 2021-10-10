from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        request drf封装的请求
        view 应用于那个视图
        obj 对象实例
        """
        # SAFE_METHODS包含了'GET', 'HEAD', 'OPTIONS'这三种方法，
        # 这三个方法是安全的，下边这个判断就是如果请求的方法在这个里边
        # 就返回True
        if request.method in permissions.SAFE_METHODS:
            return True
        # 当前登录的用户与发布的是同一个人比较结果返回
        return obj.owner == request.user


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """ 
    超级管理员具有添加，修改，删除的权限，get权限不受控制 
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
        
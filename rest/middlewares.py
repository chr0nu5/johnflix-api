from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.permissions import BasePermission


class AllowOptionsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == "OPTIONS":
            return JsonResponse({"detail": "OK"}, status=200)


class IsSuperUserOrVisibleOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return not obj.hidden

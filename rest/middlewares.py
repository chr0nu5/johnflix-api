from rest_framework.permissions import BasePermission

class IsSuperUserOrVisibleOnly(BasePermission):
    """
    Permite acesso total apenas para superusuários.
    Para usuários comuns, exibe apenas itens não ocultos (hidden=False).
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Se for superusuário, pode ver tudo
        if request.user.is_superuser:
            return True
        # Caso contrário, só pode ver se hidden=False
        return not obj.hidden

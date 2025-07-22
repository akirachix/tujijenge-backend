from rest_framework.permissions import BasePermission

class IsMamamboga(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'mamamboga')

class IsStakeholder(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'stakeholder')

def StakeholderRolePermission(*roles):
    class PermissionClass(BasePermission):
        def has_permission(self, request, view):
            stakeholder = getattr(request.user, 'stakeholder', None)
            stakeholder_role = getattr(stakeholder, 'role', '').lower() if stakeholder else ''
            allowed_roles = [role.lower() for role in roles]
            result = bool(request.user.is_authenticated and stakeholder and stakeholder_role in allowed_roles)
            return result
    return PermissionClass()

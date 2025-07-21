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
            print(f'User: {request.user}')
            print(f'Is authenticated: {request.user.is_authenticated}')
            print(f'Stakeholder: {stakeholder}')
            print(f'Stakeholder role: {stakeholder_role}')
            print(f'Allowed roles: {allowed_roles}')
            result = bool(request.user.is_authenticated and stakeholder and stakeholder_role in allowed_roles)
            print(f'Permission result: {result}')
            return result
    return PermissionClass()

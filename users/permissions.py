from rest_framework.permissions import BasePermission

class IsMamamboga(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'mamamboga')

class IsStakeholder(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'stakeholder')

class IsStakeholderRole(BasePermission):
    def __init__(self, *roles):
        self.roles = roles

    def has_permission(self, request, view):
        stakeholder = getattr(request.user, "stakeholder", None)
        return stakeholder and stakeholder.role in self.roles

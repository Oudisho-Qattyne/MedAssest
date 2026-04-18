from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrDoctorForPatients(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # Admin and doctor can list and create
        if request.method in SAFE_METHODS or request.method == 'POST':
            return request.user.role in ('admin', 'doctor')
        # For PUT/PATCH/DELETE, only admin
        return request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        # Admin can do anything
        if request.user.role == 'admin':
            return True
        # Doctor can only view
        if request.user.role == 'doctor':
            return request.method in SAFE_METHODS
        return False
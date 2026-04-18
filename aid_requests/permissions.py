from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsDoctorOrAdminForRequests(BasePermission):
    """Doctors and admins can create, list, update (except status change)"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role in ('admin', 'doctor'):
            return True
        # requests_processor can only view requests (GET)
        if request.user.role == 'requests_processor' and request.method in SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.user.role == 'doctor':
            # Doctor can update anything except status? For simplicity, allow full update.
            # But we will restrict status change in view logic.
            return True
        if request.user.role == 'requests_processor' and request.method in SAFE_METHODS:
            return True
        return False

class CanChangeRequestStatus(BasePermission):
    """Only requests_processor and admin can change request_status."""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # If the update contains 'request_status', check role
        if 'request_status' in request.data:
            return request.user.role in ('admin', 'requests_processor')
        # For other updates, allow doctor/admin
        return request.user.role in ('admin', 'doctor')
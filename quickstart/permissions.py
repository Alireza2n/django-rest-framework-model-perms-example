from rest_framework import exceptions
from rest_framework.permissions import DjangoModelPermissions


class DjangoModelPermissionsWithView(DjangoModelPermissions):
    perms_map_extra = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': [],
        'PUT': [],
        'PATCH': [],
        'DELETE': [],
    }
    
    def get_perms_map_extra(self, view):
        if hasattr(view, 'perms_map_extra'):
            return view.perms_map_extra
        return self.perms_map_extra
    
    def get_required_custom_permissions(self, method, model_cls, view):
        """
        Given a model and an HTTP method, return the list of permission
        codes that the user is required to have.
        """
        kwargs = {
            'app_label': model_cls._meta.app_label,
            'model_name': model_cls._meta.model_name
        }
        
        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)
        
        _perms_maps_extra = self.get_perms_map_extra(view)
        _out = []
        for verb in _perms_maps_extra:
            for perm in _perms_maps_extra[verb]:
                _out.append(perm % kwargs)
        return _out
    
    def has_permission(self, request, view):
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        if getattr(view, '_ignore_model_permissions', False):
            return True
        
        if not request.user or (
                not request.user.is_authenticated and self.authenticated_users_only):
            return False
        
        queryset = self._queryset(view)
        perms = self.get_required_permissions(request.method, queryset.model)
        
        # Apply custom permissions
        perms.extend(self.get_required_custom_permissions(request.method, queryset.model, view))
        
        return request.user.has_perms(perms)

from rest_framework import viewsets

from quickstart.models import Contact
from quickstart.permissions import DjangoModelPermissionsWithView
from quickstart.serializers import ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint
    """
    queryset = Contact.objects.all().order_by('-pk')
    serializer_class = ContactSerializer
    permission_classes = (DjangoModelPermissionsWithView,)

    perms_map_extra = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
    }

from rest_framework import viewsets

from apps.contact.models import Contact
from common.serializers.contact.serializers import ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().order_by('-created_at')
    serializer_class = ContactSerializer
    http_method_names = ["post"]


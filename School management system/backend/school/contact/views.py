from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import ContactMessage
from .serializers import ContactMessageSerializer


class ContactMessageCreateView(generics.CreateAPIView):
    """
    POST /api/contact/
    """

    permission_classes = [AllowAny]
    serializer_class = ContactMessageSerializer
    queryset = ContactMessage.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Thank you for contacting us. We will get back to you soon."},
            status=status.HTTP_201_CREATED,
        )
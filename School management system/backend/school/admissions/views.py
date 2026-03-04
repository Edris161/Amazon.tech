from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import AdmissionApplication
from .serializers import AdmissionApplicationSerializer


class AdmissionApplicationCreateView(generics.CreateAPIView):
    """
    POST /api/admissions/apply/
    """

    permission_classes = [AllowAny]
    serializer_class = AdmissionApplicationSerializer
    queryset = AdmissionApplication.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Your admission application has been submitted successfully."},
            status=status.HTTP_201_CREATED,
        )
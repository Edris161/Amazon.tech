from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import SiteSetting
from .serializers import SiteSettingSerializer


class SiteSettingView(APIView):
    """
    GET /api/settings/
    """

    permission_classes = [AllowAny]

    def get(self, request):
        setting = SiteSetting.objects.first()
        serializer = SiteSettingSerializer(setting, context={"request": request})
        return Response(serializer.data)
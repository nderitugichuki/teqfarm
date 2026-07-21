from rest_framework.response import Response
from rest_framework.views import APIView
from apps.common.permissions import IsFarmStaff
from .selectors import dashboard_summary


class DashboardView(APIView):
    permission_classes = (IsFarmStaff,)

    def get(self, request):
        include_financials = request.user.is_superuser or request.user.role in (
            "administrator", "manager"
        )
        return Response(dashboard_summary(include_financials=include_financials))


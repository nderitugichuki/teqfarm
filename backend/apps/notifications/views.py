from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.common.permissions import IsFarmStaff
from .models import Notification
from .serializers import NotificationSerializer
from .services import refresh_alerts


class NotificationViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsFarmStaff,)
    serializer_class = NotificationSerializer
    queryset = Notification.objects.prefetch_related("read_by")
    filterset_fields = ("alert_type", "severity", "is_resolved", "due_date")

    def list(self, request, *args, **kwargs):
        refresh_alerts()
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=("post",), url_path="read")
    def mark_read(self, request, pk=None):
        self.get_object().read_by.add(request.user)
        return Response(status=204)

    @action(detail=False, methods=("post",), url_path="read-all")
    def mark_all_read(self, request):
        for notification in self.get_queryset().filter(is_resolved=False):
            notification.read_by.add(request.user)
        return Response(status=204)

    @action(detail=False, methods=("post",), url_path="refresh")
    def refresh(self, request):
        if not (request.user.is_superuser or request.user.role in ("administrator", "manager")):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only managers can refresh system alerts.")
        return Response({"active_alerts": refresh_alerts()})

from rest_framework.viewsets import ModelViewSet


class AuditedModelViewSet(ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


from apps.common.permissions import IsAdministratorOrManager
from apps.common.viewsets import AuditedModelViewSet
from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseViewSet(AuditedModelViewSet):
    permission_classes = (IsAdministratorOrManager,)
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.select_related("created_by")
    filterset_fields = ("category", "expense_date", "payment_method")
    search_fields = ("description", "payee", "reference", "notes")
    ordering_fields = ("expense_date", "amount", "category", "created_at")


import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.expenses.serializers import ExpenseSerializer


@pytest.mark.django_db
def test_receipt_rejects_unsupported_content_type():
    receipt = SimpleUploadedFile("receipt.pdf", b"not a pdf", content_type="text/plain")
    serializer = ExpenseSerializer(data={
        "expense_date": "2025-01-01", "category": "fuel", "description": "Fuel",
        "amount": "100.00", "payment_method": "cash", "receipt": receipt,
    })
    assert not serializer.is_valid()
    assert "receipt" in serializer.errors


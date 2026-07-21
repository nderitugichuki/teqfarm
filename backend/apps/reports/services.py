from datetime import timedelta
from decimal import Decimal
from io import BytesIO
from django.db.models import Sum
from django.utils import timezone
from apps.daily_records.models import DailyFarmRecord
from apps.expenses.models import Expense
from apps.feed.models import FeedIssue
from apps.inventory.models import InventoryItem
from apps.sales.models import Sale


REPORT_TYPES = {
    "daily", "weekly", "monthly", "production", "mortality",
    "feed", "sales", "expenses", "profit-loss", "inventory",
}


def _summary(start, end):
    daily = DailyFarmRecord.objects.filter(record_date__range=(start, end)).aggregate(
        eggs=Sum("eggs_collected"), broken=Sum("broken_eggs"), dirty=Sum("dirty_eggs"),
        mortality=Sum("dead_birds"), sick=Sum("sick_birds"), feed=Sum("feed_issued_kg"),
    )
    sales = Sale.objects.filter(sale_date__range=(start, end)).aggregate(total=Sum("total_amount"))["total"] or Decimal("0")
    expenses = Expense.objects.filter(expense_date__range=(start, end)).aggregate(total=Sum("amount"))["total"] or Decimal("0")
    return [{"period_start": start, "period_end": end, "eggs": daily["eggs"] or 0,
             "broken_eggs": daily["broken"] or 0, "dirty_eggs": daily["dirty"] or 0,
             "mortality": daily["mortality"] or 0, "sick_birds": daily["sick"] or 0,
             "feed_kg": daily["feed"] or Decimal("0"), "sales": sales,
             "expenses": expenses, "profit": sales - expenses}]


def build_report(report_type, start=None, end=None):
    today = timezone.localdate()
    end = end or today
    start = start or end - timedelta(days=29)
    if report_type == "daily": start = end
    if report_type == "weekly": start = end - timedelta(days=6)
    if report_type == "monthly": start = end.replace(day=1)
    if report_type in ("daily", "weekly", "monthly", "profit-loss"):
        return _summary(start, end)
    if report_type == "production":
        return list(DailyFarmRecord.objects.filter(record_date__range=(start, end)).values(
            "record_date", "batch__batch_code", "eggs_collected", "broken_eggs", "dirty_eggs"
        ).order_by("record_date", "batch__batch_code"))
    if report_type == "mortality":
        return list(DailyFarmRecord.objects.filter(record_date__range=(start, end), dead_birds__gt=0).values(
            "record_date", "batch__batch_code", "dead_birds", "sick_birds", "observations"
        ).order_by("record_date"))
    if report_type == "feed":
        return list(FeedIssue.objects.filter(issue_date__range=(start, end)).values(
            "issue_date", "batch__batch_code", "item__name", "quantity_kg"
        ).order_by("issue_date"))
    if report_type == "sales":
        return list(Sale.objects.filter(sale_date__range=(start, end)).values(
            "sale_date", "invoice_number", "sale_type", "customer__name", "quantity",
            "unit", "total_amount", "amount_paid", "payment_status"
        ).order_by("sale_date"))
    if report_type == "expenses":
        return list(Expense.objects.filter(expense_date__range=(start, end)).values(
            "expense_date", "category", "description", "payee", "amount", "payment_method"
        ).order_by("expense_date"))
    if report_type == "inventory":
        return list(InventoryItem.objects.values(
            "sku", "name", "category", "unit", "current_stock", "reorder_level", "is_active"
        ).order_by("category", "name"))
    raise ValueError("Unsupported report type")


def export_excel(title, rows):
    from openpyxl import Workbook
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Report"
    if not rows:
        sheet.append([title, "No records found"])
    else:
        headers = list(rows[0].keys())
        sheet.append(headers)
        for row in rows:
            sheet.append([row.get(header) for header in headers])
        sheet.freeze_panes = "A2"
        sheet.auto_filter.ref = sheet.dimensions
        for column in sheet.columns:
            letter = column[0].column_letter
            sheet.column_dimensions[letter].width = min(40, max(len(str(cell.value or "")) for cell in column) + 2)
    output = BytesIO()
    workbook.save(output)
    return output.getvalue()


def export_pdf(title, rows):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    output = BytesIO()
    document = SimpleDocTemplate(output, pagesize=landscape(A4), leftMargin=24, rightMargin=24)
    elements = [Paragraph(title, getSampleStyleSheet()["Title"]), Spacer(1, 12)]
    if rows:
        headers = list(rows[0].keys())
        data = [[header.replace("_", " ").title() for header in headers]]
        data.extend([[str(row.get(header, "")) for header in headers] for row in rows])
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#257a45")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("No records found.", getSampleStyleSheet()["BodyText"]))
    document.build(elements)
    return output.getvalue()


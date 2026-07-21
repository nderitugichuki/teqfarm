from datetime import date
from django.http import HttpResponse
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.common.permissions import IsAdministratorOrManager
from .services import REPORT_TYPES, build_report, export_excel, export_pdf


def parse_date(value, field):
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError({field: "Use YYYY-MM-DD format."}) from exc


class ReportView(APIView):
    permission_classes = (IsAdministratorOrManager,)

    def get(self, request, report_type):
        if report_type not in REPORT_TYPES:
            raise ValidationError({"report_type": "Unsupported report type."})
        start = parse_date(request.query_params.get("start"), "start")
        end = parse_date(request.query_params.get("end"), "end")
        if start and end and start > end:
            raise ValidationError({"start": "Start date must not be after end date."})
        rows = build_report(report_type, start, end)
        export_format = request.query_params.get("format", "json").lower()
        title = f"TeqFarm {report_type.replace('-', ' ').title()} Report"
        if export_format == "xlsx":
            response = HttpResponse(export_excel(title, rows), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response["Content-Disposition"] = f'attachment; filename="teqfarm-{report_type}.xlsx"'
            return response
        if export_format == "pdf":
            response = HttpResponse(export_pdf(title, rows), content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="teqfarm-{report_type}.pdf"'
            return response
        if export_format != "json":
            raise ValidationError({"format": "Use json, xlsx, or pdf."})
        return Response({"report_type": report_type, "count": len(rows), "results": rows})


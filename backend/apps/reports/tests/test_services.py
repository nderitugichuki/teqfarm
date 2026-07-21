from apps.reports.services import export_excel, export_pdf

def test_excel_export_is_an_xlsx_archive():
    content = export_excel("Test", [{"name": "Eggs", "quantity": 30}])
    assert content.startswith(b"PK")

def test_pdf_export_has_pdf_signature():
    content = export_pdf("Test", [{"name": "Eggs", "quantity": 30}])
    assert content.startswith(b"%PDF")


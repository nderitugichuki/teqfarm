from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    detail = response.data
    message = detail.get("detail") if isinstance(detail, dict) else None
    response.data = {
        "success": False,
        "message": str(message or "The request could not be completed."),
        "errors": detail,
    }
    return response


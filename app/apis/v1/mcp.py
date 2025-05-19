from flask import request, Blueprint
from services.websearch.request import WebSearchRequest

from exc import httperrors


VERSION = "v1"
ROUTE = "invoke"

bp = Blueprint(ROUTE, __name__)


def url(route: str) -> str:
    return f"/api/{VERSION}/mcp/{route}"


@bp.route(url(f"{ROUTE}"), methods=["POST"])
def handle_mcp_invoke():
    req = WebSearchRequest(**request.get_json())
    print(req)
    match request.method:
        case "POST":
            return 200, "ok"

    return httperrors.not_implemented()

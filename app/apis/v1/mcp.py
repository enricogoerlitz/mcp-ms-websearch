from flask import request, Blueprint
from exc import httperrors
from services.rest.v1.mcp import websearch_service


VERSION = "v1"
ROUTE = "invoke"

bp = Blueprint(ROUTE, __name__)


def url(route: str) -> str:
    return f"/api/{VERSION}/mcp/websearch/{route}"


@bp.route(url(f"{ROUTE}"), methods=["POST"])
def handle_mcp_invoke():
    match request.method:
        case "POST":
            return websearch_service.handle_mcp_invoke(request.get_json())

    return httperrors.not_implemented()

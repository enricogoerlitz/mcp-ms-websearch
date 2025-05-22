from flask import request, Blueprint

from exc import httperrors


VERSION = "v1"
ROUTE = "health"

bp = Blueprint(ROUTE, __name__)


def url(route: str) -> str:
    return f"/api/{VERSION}/{route}"


@bp.route(url(f"{ROUTE}"), methods=["GET"])
def handle_chats():
    match request.method:
        case "GET":
            return 200, "ok"

    return httperrors.not_implemented()
